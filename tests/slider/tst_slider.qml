import QtQuick
import QtTest

TestCase {
    name: "PowerProfileSlider"
    when: windowShown

    Main {
        id: app
        visible: true
    }

    function test_interaction() {
        const slider = findChild(app, "testPowerSlider");
        const setter = findChild(app, "testSetEngine");
        verify(slider !== null);
        verify(setter !== null);
        tryVerify(function() { return slider.enabled; });
        compare(slider.value, 1);
        compare(setter.lastCommand, "");

        mousePress(slider, slider.width / 2, slider.height / 2);
        mouseMove(slider, slider.width - 4, slider.height / 2, 20);
        compare(setter.lastCommand, "");
        mouseRelease(slider, slider.width - 4, slider.height / 2);
        tryVerify(function() {
            return setter.lastCommand.includes("set performance");
        });
        tryVerify(function() { return slider.enabled; });
        compare(slider.value, 1);

        app.requestActivate();
        slider.forceActiveFocus();
        tryVerify(function() { return slider.activeFocus; });
        keyClick(Qt.Key_Left);
        tryVerify(function() {
            return setter.lastCommand.includes("set power-saver");
        });
        tryVerify(function() { return slider.enabled; });

        const message = findChild(app, "testPowerMessage");
        const reader = findChild(app, "testReadEngine");
        verify(message !== null);
        verify(reader !== null);
        setter.mockFailure = true;
        mouseClick(slider, slider.width - 4, slider.height / 2);
        tryVerify(function() { return message.visible; });
        tryVerify(function() { return slider.enabled; });
        verify(message.text.includes("Unable to change"));

        setter.mockFailure = false;
        mouseClick(slider, slider.width - 4, slider.height / 2);
        tryVerify(function() { return slider.enabled && !message.visible; });

        reader.mockFailure = true;
        reader.exec("/kfocus-power-profile get");
        tryVerify(function() { return !slider.enabled && message.visible; });
        verify(message.text.includes("Unable to read"));
        reader.mockFailure = false;
        reader.exec("/kfocus-power-profile get");
        tryVerify(function() { return slider.enabled && !message.visible; });
    }
}
