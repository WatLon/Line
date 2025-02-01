#pragma once

#include <QMainWindow>
#include <QSystemTrayIcon>
#include <QMenu>

#include <QMouseEvent>
#include <QCloseEvent>

#include <QFile>
#include <QTextStream>
#include <QStandardPaths>
#include <QFileDialog>
#include <QSettings>

#include <QProcess>
#include <QTimer>

#include <QFontDatabase>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    // Choose Config Button logic
    void on_configButton_clicked();

    // Connect Button logic
    void on_connectButton_clicked();

    // Window Controls Buttons handlers
    void on_controlWindowCloseButton_clicked();
    void on_controlWindowMinimizeButton_clicked();

    // AutoStart CheckBox handler
    void on_autoStartCheckBox_clicked();

protected:
    void closeEvent(QCloseEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;

private:
    // UI
    Ui::MainWindow *ui;

    // Choose Config Button logic
    void startTimer(QString);
    void copyConfig(QString);

    QString getConfigPath();

    // Connect Button logic
    void runWinws();
    void stopWinws();

    QProcess *winwsProcess;
    QString winwsPath;
    QStringList winwsArgs;
    QSettings *config;

    // Startup logic
    void startUpOn();
    void startUpOff();
    bool isInStartUp();

    QString shortcutPath;

    // Tray Icon logic
    void createTrayIcon();

    QSystemTrayIcon *trayIcon;
    QMenu *trayIconMenu;
    bool closeFromTray;

    // Dragging logic
    bool dragging;
    QPoint dragStartPosition;
};
