#include "mainwindow.h"

#include <QApplication>


// Initialize MainWindow
void initializeMainWindow(MainWindow* window)
{
    window->setWindowFlag(Qt::FramelessWindowHint);
    window->setAttribute(Qt::WA_TranslucentBackground);
    window->setWindowIcon(QIcon(":/assets/bloom.png"));
}

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow window;
    initializeMainWindow(&window);

    window.show();
    return a.exec();
}
