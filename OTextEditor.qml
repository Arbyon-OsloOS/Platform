import QtQuick 2.12
import QtQuick.Controls 2.12

TextArea {
    property string accent: "#0088ff" // Nice blue
    property string accentAlt: "#00ffff" // Another blue
    id: t
    //x: 3
    //y: 3
    //width: parent.width - 6
    //height: parent.height - 6
    wrapMode: TextArea.WordWrap
    readOnly: false
    Component.onCompleted: this.focus = true;
    background: Rectangle {
        radius: 8
        border.color: parent.focus ? accent : "#888888"
    }
    selectByMouse: true
    persistentSelection: true
    MouseArea {
        acceptedButtons: "RightButton"
        onPressed: {
            contextMenu.createObject(t, {}).show()
        }
    }
    Component {
        id: contextMenu
        Menu {
            id: m
            Component.onCompleted: m.open();
            MenuItem {
                text: qsTr("Cut")
                action: t.cut()
            }
            MenuItem {
                text: qsTr("Copy")
                action: t.copy()
            }
            MenuItem {
                text: qsTr("Paste")
                action: t.paste()
                enabled: t.canPaste
            }
            MenuItem {
                text: qsTr("Undo")
                action: t.undo()
                enabled: t.canUndo
            }
            MenuItem {
                text: qsTr("Redo")
                action: t.redo()
                enabled: t.canRedo
            }
        }
    }
}
