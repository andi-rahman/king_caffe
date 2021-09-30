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
                const order = this.env.pos.get_order();
                if (order.hasChangesToPrint()) {
                    const isPrintSuccessful = await order.printChanges();
                    if (isPrintSuccessful) {
                        order.saveChanges();
                    } else {
                        await this.showPopup('ErrorPopup', {
                            title: 'Printing failed',
                            body: 'Failed in printing the changes in the order',
                        });
                    }
                }
                // await super.printReceipt();
                // this.currentOrder._printed = false;
            }
        }
        BarScreens.template = 'BarScreens';
        return BarScreens;
    };

    Registries.Component.addByExtending(BarScreens, ReceiptScreen);

    return BarScreens;
});
