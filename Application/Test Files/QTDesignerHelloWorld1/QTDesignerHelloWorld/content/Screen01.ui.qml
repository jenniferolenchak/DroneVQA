

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick 6.2
import QtQuick.Controls 6.2
import QTDesignerHelloWorld

Rectangle {
    width: Constants.width
    height: Constants.height

    color: Constants.backgroundColor

    Item {
        id: item1
        x: 26
        y: 20
        width: 1118
        height: 620

        BorderImage {
            id: borderImage
            x: 100
            y: 48
            width: 478
            height: 538
            source: "../../../../../../../../Pictures/Profile Photo - Cropped.JPG"

            StackView {
                id: stackView
                x: 272
                y: 74
                width: 724
                height: 518

                Loader {
                    id: loader
                    x: 624
                    y: 64
                    width: 200
                    height: 200
                }

                Rectangle {
                    id: rectangle
                    x: 122
                    y: 216
                    width: 200
                    height: 200
                    color: "#ffffff"
                }
            }
        }
    }

    Control {
        id: control
        x: 1026
        y: 646
        width: 318
        height: 316

        RoundButton {
            id: roundButton
            x: 152
            y: -120
            width: 280
            height: 202
            text: "+"
            transformOrigin: Item.TopLeft
        }
    }

    Control {
        id: control1
        x: 622
        y: 878
    }

    PageIndicator {
        id: pageIndicator
        x: 392
        y: 896
        count: 3
    }

    Dial {
        id: dial
        x: 844
        y: 848
    }

    Image {
        id: image
        x: 1378
        y: 828
        width: 100
        height: 100
        source: "qrc:/qtquickplugin/images/template_image.png"
        fillMode: Image.PreserveAspectFit
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.5}
}
##^##*/

