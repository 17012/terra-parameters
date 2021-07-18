"use strict";
exports.__esModule = true;
var terra_js_1 = require("@terra-money/terra.js");
// connect to soju testnet
var terra = new terra_js_1.LCDClient({
    URL: 'https://tequila-lcd.terra.dev',
    chainID: 'tequila-0004'
});
// To use LocalTerra
// const terra = new LCDClient({
//   URL: 'http://localhost:1317',
//   chainID: 'localterra'
// });
// get the current swap rate from 1 TerraUSD to TerraKRW
var offerCoin = new terra_js_1.Coin('uusd', '1000000');
terra.market.swapRate(offerCoin, 'ukrw').then(function (c) {
    console.log(offerCoin.toString() + " can be swapped for " + c.toString());
});
