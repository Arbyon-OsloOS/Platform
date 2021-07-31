import QtQuick 2.12
import QtQuick.Controls 2.12

Frame {
    property string accent: "#0088ff" // Nice blue
    property string accentAlt: "#00ffff" // Another blue
    x: 3
    y: 67
    height: parent.height - 70
    width: parent.width - 6
    background: Rectangle {
        radius: 8
        border.color: "#888888"
        color: "white"
    }
}
