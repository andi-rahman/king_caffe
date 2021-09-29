odoo.define('king_pos.BarScreens', function (require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');

    const BarScreens = (ReceiptScreen) => {
        class BarScreens extends ReceiptScreen {
            confirm() {
                this.props.resolve({ confirmed: true, payload: null });
                this.trigger('close-temp-screen');
            }
            whenClosing() {
                this.confirm();
            }
            /**
             * @override
             */
            async printReceipt() {
                await super.printReceipt();
                this.currentOrder._printed = false;
            }
        }
        BarScreens.template = 'BarScreens';
        return BarScreens;
    };

    Registries.Component.addByExtending(BarScreens, ReceiptScreen);

    return BarScreens;
});
