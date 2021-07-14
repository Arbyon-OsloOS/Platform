import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12

Window {
    property string accent: "#0088ff" // Nice blue
    property string accentAlt: "#00ffff" // Another blue
    width: 640
    height: 480
    visible: true
    color: "transparent"
    flags: "FramelessWindowHint"
    id: wind

    Frame {
        x: 0
        y: 0
        background: Rectangle {
            color: "#bbbbbb"
            //color: "#aaffffff" // looks ugly as fuuuuuuuuuuuuck
            radius: 10
            border.color: "transparent"
        }
        width: parent.width - 0
        height: parent.height - 0
        padding: 0
        Frame {
            x: 0
            y: 1
            width: parent.width
            height: 30
            background: Rectangle {
                radius: 10
                border.color: "white"
                gradient: Gradient {
                    GradientStop {position: 0; color: wind.active ? "#eeeeee" : "#999999"}
                    GradientStop {position: 1/3; color: wind.active ? "#dddddd" : "#aaaaaa"}
                    GradientStop {position: 1; color: "#bbbbbb"}
                    orientation: Gradient.Vertical
                }
            }
        }
        Frame {
            x: 0
            y: 11
            width: parent.width
            height: 20
            background: Rectangle {
                border.color: "#bbbbbb"
                border.width: 0
                gradient: Gradient {
                    GradientStop {position: 0; color: wind.active ? "#dddddd" : "#aaaaaa"}
                    GradientStop {position: 0.5; color: wind.active ? "#cccccc" : "#b8b8b8"}
                    GradientStop {position: 1; color: "#bbbbbb"}
                    orientation: Gradient.Vertical
                }
            }
        }
        Text { // window title
            x: 0
            y: 0
            width: parent.width
            height: 32
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: wind.title
            color: "#3c3c3c"
            font.bold: true
            font.pointSize: 9
        } // you can drag the window
        MouseArea {
            x: 0
            y: 0
            width: parent.width
            height: 67 //32 // We want to be able to drag the toolbar
            property int t_X: 0
            property int t_Y: 0
            function startWinDrag(mouse){
                t_X = mouse.x
                t_Y = mouse.y
                cursorShape = Qt.ClosedHandCursor
            }
            function draggy(mouse) {
                wind.x += mouse.x - t_X
                wind.y += mouse.y - t_Y
                if (wind.visibility == Window.Maximized) {
                    wind.showNormal();
                }
                if (mouse.y + wind.y <= 0 && wind.y <= 0) { // MAY perform, but DOES it???
                    wind.showMaximized()
                }
            }
            onPositionChanged: draggy(mouse)
            onPressed: startWinDrag(mouse)
            onReleased: cursorShape = Qt.ArrowCursor
        }
        // Window buttons
        Frame {
            x: 4
            y: 4
            width: 68
            height: 24
            background: Rectangle {
                border.color: "#ffffff"
                radius: 12
                gradient: Gradient {
                    GradientStop {position: 0; color: "#e0e0e0"}
                    GradientStop {position: 0.5; color: "#f0f0f0"}
                    GradientStop {position: 1; color: "#e0e0e0"}
                }
            }
            padding: 0
            AbstractButton {
                x: 2
                y: 2
                width: 20
                height: 20
                background: Rectangle {
                    border.color: parent.focus ? "#ffffff" : "#888888"
                    radius: 10
                    gradient: Gradient {
                        GradientStop {position: 0; color: "#ff8888"}
                        GradientStop {position: 1; color: "#aa0000"}
                        orientation: Gradient.Vertical
                    }
                }
                Image {
                    anchors.fill: parent
                    source: "./ui/icons/close.png"
                    visible: c_.containsMouse
                }
                MouseArea {
                    anchors.fill: parent
                    id: c_
                    hoverEnabled: true
                    onClicked: wind.close()
                }
            }
            AbstractButton {
                x: 24
                y: 2
                width: 20
                height: 20
                background: Rectangle {
                    border.color: parent.focus ? "#ffffff" : "#888888"
                    radius: 10
                    gradient: Gradient {
                        GradientStop {position: 0; color: "#ffcc88"}
                        GradientStop {position: 1; color: "#ff8800"}
                        orientation: Gradient.Vertical
                    }
                }
                Image {
                    anchors.fill: parent
                    source: "./ui/icons/minimise.png"
                    visible: i_.containsMouse
                }
                MouseArea {
                    onClicked: wind.showMinimized()
                    hoverEnabled: true
                    id: i_
                    anchors.fill: parent
                }
            }
            AbstractButton {
                x: 46
                y: 2
                width: 20
                height: 20
                background: Rectangle {
                    border.color: parent.focus ? "#ffffff" : "#888888"
                    radius: 10
                    gradient: Gradient {
                        GradientStop {position: 0; color: "#88ff88"}
                        GradientStop {position: 1; color: "#008800"}
                        orientation: Gradient.Vertical
                    }
                }
                Image {
                    anchors.fill: parent
                    source: "./ui/icons/maximise.png"
                    visible: m_.containsMouse
                }

                MouseArea {
                    id: m_
                    hoverEnabled: true
                    anchors.fill: parent
                    onClicked: {
                        if (wind.visibility == Window.Windowed)
                            wind.showMaximized();
                        else
                            wind.showNormal();
                    }
                }
            }
        }
        // Resize grip
        Image {
            x: parent.width - 20
            y: parent.height - 20
            width: 20
            height: 20
            source: "./ui/icons/resize.png"
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.SizeFDiagCursor
                property int t_X: 0
                property int t_Y: 0
                onPositionChanged: draggy(mouse)
                onPressed: startWinDrag(mouse)

                function startWinDrag(mouse){
                    t_X = mouse.x
                    t_Y = mouse.y
                }
                function draggy(mouse) {
                    wind.width += mouse.x - t_X
                    wind.height += mouse.y - t_Y
                }
            }
        }
    }// end of window
}// end of drop shadow around window
