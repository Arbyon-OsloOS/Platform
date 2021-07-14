import QtQuick 2.12
import QtQuick.Controls 2.12

Button {
    property string accent: "#0088ff" // Nice blue
    property string accentAlt: "#00ffff" // Another blue
    height: 30
    width: 30
    background: Rectangle {
        radius: 5
        border.color: parent.focus ? accent : "#888888"
        gradient: Gradient {
            //GradientStop {position: 0; color: "#cccccc"}
            GradientStop {position: 0; color: "#ffffff"}
            GradientStop {position: 1; color: "#cccccc"}
            orientation: Gradient.Vertical
        }
        property Gradient normalGradient: Gradient {
            //GradientStop {position: 0; color: "#cccccc"}
            GradientStop {position: 0; color: "#ffffff"}
            GradientStop {position: 1; color: "#cccccc"}
            orientation: Gradient.Vertical
        }
        property Gradient pushedGradient: Gradient {
            //GradientStop {position: 0; color: "#eeeeee"}
            GradientStop {position: 0; color: "#cccccc"}
            GradientStop {position: 1; color: "#ffffff"}
            orientation: Gradient.Vertical
        }
    }
    MouseArea {
        anchors.fill: parent
        onPressed: parent.background.gradient = parent.background.pushedGradient
        onReleased: parent.background.gradient = parent.background.normalGradient
        onClicked: parent.onClicked()
    }
}
