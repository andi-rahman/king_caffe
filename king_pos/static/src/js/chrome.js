odoo.define('king_pos.ProductScreen', function (require) {
"use strict";


const TicketButton = require('point_of_sale.TicketButton');
const ProductScreen = require('point_of_sale.ProductScreen');
const Registries = require('point_of_sale.Registries');
const { posbus } = require('point_of_sale.utils');
var models = require('point_of_sale.models');
var exports = {};


var _super_orderline = models.Orderline.prototype;
models.Orderline = models.Orderline.extend({
    initialize: function(attr,options) {
        _super_orderline.initialize.apply(this,arguments);
        this.is_food = this.product.is_food;
        this.is_drink = this.product.is_drink;
    },
    get_food: function(){
        return this.is_food;
    },
    get_drink: function(){
        return this.is_drink;
    },
    get_note: function(){
        return this.note;
    },
    get_client: function(){
        console.log("POS")
        console.log(this)
        return this.order.get_client();
    },
    export_for_printing: function(){
        return {
            id: this.id,
            client:             this.get_client(),
            quantity:           this.get_quantity(),
            unit_name:          this.get_unit().name,
            is_in_unit:         this.get_unit().id == this.pos.uom_unit_id,
            price:              this.get_unit_display_price(),
            discount:           this.get_discount(),
            product_name:       this.get_product().display_name,
            product_name_wrapped: this.generate_wrapped_product_name(),
            price_lst:          this.get_lst_price(),
            display_discount_policy:    this.display_discount_policy(),
            price_display_one:  this.get_display_price_one(),
            price_display :     this.get_display_price(),
            price_with_tax :    this.get_price_with_tax(),
            price_without_tax:  this.get_price_without_tax(),
            price_with_tax_before_discount:  this.get_price_with_tax_before_discount(),
            tax:                this.get_tax(),
            product_description:      this.get_product().description,
            product_description_sale: this.get_product().description_sale,
            pack_lot_lines:      this.get_lot_lines(),
            is_food:            this.get_food(), 
            is_drink:            this.get_drink(),
            note:            this.get_note(),
        };
    },
})

// override
models.load_fields('product.product',['is_food','is_drink']);

models.load_models([{
    model:  'res.users',
    fields: ['name','company_id', 'id', 'groups_id', 'lang'],
    domain: function(self){ return [['company_ids', 'in', self.config.company_id[0]],'|', ['groups_id','=', self.config.group_pos_manager_id[0]],['groups_id','=', self.config.group_pos_user_id[0]]]; },
    loaded: function(self,users){
        users.forEach(function(user) {
            user.role = 'cashier';
            user.groups_id.some(function(group_id) {
                if (group_id === self.config.group_pos_manager_id[0]) {
                    user.role = 'manager';
                    return true;
                }
            });
            if (user.id === self.session.uid) {
                self.user = user;
                self.employee.name = user.name;
                self.employee.role = user.role;
                self.employee.user_id = [user.id, user.name];
            }
        });
        self.users = users;
        self.employees = [self.employee];
        self.set_cashier(self.employee);
    }
}]);

const KingProductScreen = (ProductScreen) =>
    class extends ProductScreen {
        // Override
        _onClickPay() {
            var password = this.env.pos.config.pin
            if (this.props.isTicketScreenShown) {
                posbus.trigger('ticket-button-clicked');
            } else {
                if (password) {
                    this.showPopup('NumberPopup', {
                        startingValue: 0,
                        isPassword: true,
                        title: this.env._t('Input Pin'),
                    }).then(({ confirmed, payload: pw }) => {
                        if (confirmed) {
                            console
                            if (pw !== password){
                                this.showPopup('ErrorPopup', {
                                    title: this.env._t('Incorrect Password'),
                                });
                            } else {
                                this.showScreen('PaymentScreen');
                            }
                        }
                    });
                } else {
                    this.showScreen('PaymentScreen');
                }

            }
        }
    };

Registries.Component.extend(ProductScreen, KingProductScreen);

return ProductScreen;

});
