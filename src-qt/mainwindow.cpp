#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <QFile>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QString>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    getConfig();
    getIssues();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::getConfig()
{
    QString jsondata;
    QFile file;
    file.setFileName("config.json");
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    jsondata = file.readAll();
    file.close();

    QJsonDocument qdoc = QJsonDocument::fromJson(jsondata.toUtf8());
    QJsonObject qobj = qdoc.object();
    QJsonValue user = qobj.value(QString("user"));
    QJsonValue repo = qobj.value(QString("repo"));
    QJsonValue token = qobj.value(QString("token"));

    //qWarning() << val;
    qDebug() << user << "\n" << repo << "\n" << token;


    /*
    QJsonDocument d = QJsonDocument::fromJson(val.toUtf8());
    QJsonObject sett2 = d.object();
    QJsonValue value = sett2.value(QString("user"));
    qWarning() << value;
    QJsonObject item = value.toObject();
    qWarning() << tr("QJsonObject of description: ") << item;
    */
}

void MainWindow::getIssues()
{
    qDebug() << "Starting getIssues()";

    QString jsonData;
    QFile file("issues.json");
    /*
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    QByteArray jsondata = file.readAll();
    file.close();
    */
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    jsonData = file.readAll();
    file.close();

    QJsonDocument jsonDoc = QJsonDocument::fromJson(jsonData.toUtf8());
    //qDebug() << jsonDoc;
    //QJsonObject jsonObj = jsonDoc.array();
    //qDebug() << jsonObj["title"];
    QJsonArray jsonArr = jsonDoc.array();
    //qDebug() << jsonArr;

    foreach (const QJsonValue & value, jsonArr) {
        QJsonObject obj = value.toObject();
        //qDebug() << "Title: " << obj["title"] << "\n\n";
        QString username = obj["login"].toString();
        QString issue_title = obj["title"].toString();
        QString issue = "#" + obj["number"].toString() + " - " + obj["title"].toString() + " - ";

        QJsonArray userArr = obj["user"].array();
        qDebug() << userArr["avatar_url"];

        ui->listWidget->addItem(issue);
    }



    /*
    QJsonDocument document = QJsonDocument::fromJson(jsonData);
    QJsonObject object = document.object();

    QJsonValue value = object.value("user");
    QJsonArray array = value.toArray();
    foreach (const QJsonValue & v, array)
    {
        qDebug() << v.toObject().value("id").toInt();
    }
    qDebug() << object;
    */
}
