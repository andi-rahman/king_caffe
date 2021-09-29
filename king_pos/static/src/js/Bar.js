odoo.define('king_pos.Bar', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class PrintBar extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        async onClick() {
            const order = this.env.pos.get_order();
            if (order.get_orderlines().length > 0) {
                await this.showTempScreen('BarScreens');
            } else {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Nothing to Print'),
                    body: this.env._t('There are no order lines'),
                });
            }
        }
    }
    PrintBar.template = 'PrintBar';

    ProductScreen.addControlButton({
        component: PrintBar,
        condition: function() {
            return this.env.pos.config.iface_bar;
        },
    });

    Registries.Component.add(PrintBar);

    return PrintBar;
});
