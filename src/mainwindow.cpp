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
    winwsPath = "bin/winws.exe";
    winwsArgs = config->value("Winws/arguments").toString().split(" ");
    shortcutPath = QStandardPaths::writableLocation(QStandardPaths::ApplicationsLocation) + "/Startup/Line.lnk";

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

    // DEBUG ==============================
    // connect(winwsProcess, &QProcess::readyReadStandardError, this, [&]() -> void {
    //     qDebug() << winwsProcess->readAllStandardError();
    // });
    // connect(winwsProcess, &QProcess::finished, this, [](int exitCode, QProcess::ExitStatus exitStatus) -> void {
    //     qDebug() << exitCode;
    // });
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
        MainWindow::stopWinws();
    } else {
        findAndKillProcess("winws.exe");
        ui->connectButton->setText("Connected");
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
    QAction *quitAction = new QAction("Закрыть", this);

    connect(restoreAction, &QAction::triggered, this, [this]() -> void {
        closeFromTray = false;
        show();
    });
    connect(quitAction, &QAction::triggered, qApp, [this]() -> void {
        closeFromTray = true;
        QApplication::quit();
    });

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
