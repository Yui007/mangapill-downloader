import QtQuick
import QtQuick.Controls
import "../theme"

/**
 * ToggleSwitch - iOS-style animated toggle switch
 */
Switch {
    id: root
    
    property color activeColor: Theme.accentPrimary
    property color inactiveColor: "#4A4A5A"  // Brighter gray for visibility
    
    implicitWidth: 56
    implicitHeight: 30
    
    indicator: Rectangle {
        id: track
        width: root.implicitWidth
        height: root.implicitHeight
        radius: height / 2
        color: root.checked ? root.activeColor : root.inactiveColor
        border.color: root.checked ? Qt.lighter(root.activeColor, 1.2) : "#6B6B8D"
        border.width: 2
        
        Behavior on color {
            ColorAnimation { duration: Theme.animNormal }
        }
        
        Behavior on border.color {
            ColorAnimation { duration: Theme.animNormal }
        }
        
        // Knob
        Rectangle {
            id: knob
            width: 22
            height: 22
            radius: height / 2
            anchors.verticalCenter: parent.verticalCenter
            x: root.checked ? parent.width - width - 3 : 3
            color: Theme.textPrimary
            
            // Inner shadow for depth
            Rectangle {
                anchors.fill: parent
                anchors.margins: 2
                radius: parent.radius
                color: "transparent"
                border.color: Qt.rgba(0, 0, 0, 0.1)
                border.width: 1
            }
            
            Behavior on x {
                NumberAnimation {
                    duration: Theme.animNormal
                    easing.type: Easing.OutBack
                    easing.overshoot: 1.5
                }
            }
            
            // Scale bounce on change
            scale: root.pressed ? 0.9 : 1.0
            
            Behavior on scale {
                NumberAnimation {
                    duration: Theme.animFast
                    easing.type: Easing.OutCubic
                }
            }
        }
        
        // Glow when active
        layer.enabled: root.checked
        layer.effect: Item {
            // Shadow approximation
            Rectangle {
                anchors.fill: parent
                anchors.margins: -4
                radius: parent.height / 2 + 4
                color: "transparent"
                border.color: Qt.rgba(
                    root.activeColor.r,
                    root.activeColor.g,
                    root.activeColor.b,
                    0.4
                )
                border.width: 4
            }
        }
    }
    
    background: Item {}
}
