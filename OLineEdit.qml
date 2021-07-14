import QtQuick 2.12
import QtQuick.Controls 2.12

TextField {
    property string accent: "#0088ff" // Nice blue
    property string accentAlt: "#00ffff" // Another blue
    height: 30
    width: 200
    background: Rectangle {
        radius: 8
        border.color: parent.focus ? accent : "#888888"
        gradient: Gradient {
            GradientStop {position: 0; color: "#dddddd"}
            GradientStop {position: 1; color: "#eeeeee"}
            orientation: Gradient.Vertical
        }
    }
}
