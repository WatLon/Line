#include "mainwindow.h"
#include "../forms/ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    winwsProcess(new QProcess(this)),
    config(new QSettings("config/config.ini", QSettings::IniFormat, this))
{
    ui->setupUi(this);
    dragging = false;
    closeFromTray = false;
    winwsPath = "./bin/winws.exe";
    winwsArgs = config->value("Winws/arguments").toString().split(" ");
    shortcutPath = QStandardPaths::writableLocation(QStandardPaths::ApplicationsLocation) + "/Startup/Line.lnk";

    int idDotMatrix = QFontDatabase::addApplicationFont(":/fonts/Dot-Matrix.ttf");
    int idNTypeRegular    = QFontDatabase::addApplicationFont(":/fonts/NType82-Regular.otf");
    if (idDotMatrix < 0 || idNTypeRegular < 0) {
        qDebug() << "Failed to load fonts from resources!";
    } else {
        qDebug() << "Fonts successfully loaded!";
    }

    QStringList dotMatrixFamilies = QFontDatabase::applicationFontFamilies(idDotMatrix);
    QStringList ntypeRegularFamilies = QFontDatabase::applicationFontFamilies(idNTypeRegular);

    if (!dotMatrixFamilies.isEmpty()) {
        QFont dotMatrix(dotMatrixFamilies.at(0), 10);

        ui->configButton->setFont(dotMatrix);
        ui->connectButton->setFont(dotMatrix);
        ui->autoStartCheckBox->setFont(dotMatrix);
    }

    if (!ntypeRegularFamilies.isEmpty()) {
        QFont ntypeRegular(ntypeRegularFamilies.at(0), 50);
        ui->titleLable->setFont(ntypeRegular);
    }

    createTrayIcon();

    trayIcon->show();
    ui->autoStartCheckBox->setChecked(isInStartUp());
}

MainWindow::~MainWindow()
{
    delete ui;
}

// Config Button logic
QString MainWindow::getConfigPath()
{
    return QFileDialog::getOpenFileName(this, "Choose config path", "./", "Config Files (*.ini)");
}

void MainWindow::startTimer(QString text)
{
    QTimer *timer = new QTimer(this);
    connect(timer, &QTimer::timeout, [this, timer, text]() {
        ui->configButton->setText(text);

        timer->stop();
        timer->deleteLater();
    });

    timer->setSingleShot(true);
    timer->start(3000);
}

void MainWindow::copyConfig(QString configPath)
{
    QString destinationPath = "./config/config.ini";

    QDir configDir;
    if (!configDir.exists("./config")) {
        configDir.mkpath("./config");
    }

    if (QFile::exists(destinationPath))
    {
        QFile::remove(destinationPath);
    }

    if (QFile::copy(configPath, destinationPath)) {
        ui->configButton->setText("Success!");
        startTimer("Choose config file");
    } else {
        ui->configButton->setText("Error!");
        startTimer("Choose config file");
    }
}

void MainWindow::on_configButton_clicked()
{
    QString configPath = getConfigPath();

    if (!configPath.isEmpty())
    {
        copyConfig(configPath);
    }
}

// Connect Button logic
void MainWindow::runWinws()
{
    winwsProcess->start(winwsPath, winwsArgs);
    winwsProcess->waitForStarted();
}

void findAndKillProcess(QString target)
{
    QProcess process;
    process.startCommand("tasklist");
    process.waitForFinished();

    QString output = process.readAllStandardOutput();
    if (output.contains(target))
    {
        QString command = "taskkill /F /IM " + target;
        process.startCommand(command);
        process.waitForFinished();
    }
}

void MainWindow::stopWinws()
{
    winwsProcess->close();
}

void MainWindow::on_connectButton_clicked()
{
    if (winwsProcess->isOpen())
    {
        ui->connectButton->setText("Connect");
        trayIconMenu->actions().at(0)->setText("Подключиться");
        MainWindow::stopWinws();
    } else {
        findAndKillProcess("winws.exe");
        ui->connectButton->setText("Connected");
        trayIconMenu->actions().at(0)->setText("Отключиться");
        MainWindow::runWinws();
    }
}

// AutoStart logic
bool MainWindow::isInStartUp() {
    QFile file(shortcutPath);

    return file.exists();
}

void MainWindow::startUpOn() {
    QFile::link("Line.exe", shortcutPath);
}

void MainWindow::startUpOff() {
    QFile file(shortcutPath);

    file.remove();
}

void MainWindow::on_autoStartCheckBox_clicked()
{
    if (ui->autoStartCheckBox->isChecked()) {
        startUpOn();
    } else {
        startUpOff();
    }
}


// Tray Icon logic
void MainWindow::createTrayIcon()
{
    trayIconMenu = new QMenu();
    QAction *restoreAction = new QAction("Развернуть", this);
    QAction *switchConnectionAction = new QAction("Подключиться", this);
    QAction *quitAction = new QAction("Закрыть", this);

    connect(switchConnectionAction, &QAction::triggered, this, [this, switchConnectionAction]() -> void {
        QString text;
        if (winwsProcess->isOpen()) {
            text = "Подключиться";
            ui->connectButton->setText("Connect");
            stopWinws();
        } else {
            text = "Отключиться";
            ui->connectButton->setText("Connected");
            runWinws();
        }

        switchConnectionAction->setText(text);
    });

    connect(restoreAction, &QAction::triggered, this, [this]() -> void {
        closeFromTray = false;
        show();
    });
    connect(quitAction, &QAction::triggered, qApp, [this]() -> void {
        closeFromTray = true;
        QApplication::quit();
    });

    trayIconMenu->addAction(switchConnectionAction);
    trayIconMenu->addAction(restoreAction);
    trayIconMenu->addAction(quitAction);

    trayIcon = new QSystemTrayIcon(QIcon(":/assets/bloom.png"), this);
    trayIcon->setContextMenu(trayIconMenu);
}

// Dragging logic
void MainWindow::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton)
    {
        dragging = true;
        dragStartPosition = event->globalPosition().toPoint() - frameGeometry().topLeft();
    }
}

void MainWindow::mouseMoveEvent(QMouseEvent *event)
{
    if (dragging)
    {
        move(event->globalPosition().toPoint() - dragStartPosition);
    }
}

void MainWindow::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton)
    {
        dragging = false;
    }
}

// Window Controls Buttons logic
void MainWindow::on_controlWindowCloseButton_clicked()
{
    close();
}

void MainWindow::on_controlWindowMinimizeButton_clicked()
{
    showMinimized();
}


void MainWindow::closeEvent(QCloseEvent *event)
{
    if (closeFromTray)
    {
        event->accept();
    } else {
        hide();

        trayIcon->show();
        trayIcon->showMessage("Line", "The application continues to run in the background.", QSystemTrayIcon::Information, 2000);

        closeFromTray = true;

        event->ignore();
    }
}
