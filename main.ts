import { LCDClient, Coin,TxAPI, MnemonicKey } from '@terra-money/terra.js';
import axios from 'axios'
import fs from 'fs'

type Rate = {
  denom: string,
  amount: string,
}

type ExchangeRate = {
  height: String,
  result: Rate[]
}

type StoreRate = {
  [height:string]: ExchangeRate[]
}

const rates: StoreRate = JSON.parse(fs.readFileSync("./exchange_rates.json",'utf-8'))
let latestHeight

if(rates)
  latestHeight = Math.max(...Object.keys(rates).map(height => parseInt(height)))

console.log(latestHeight)

const data = fs.readFileSync('TS_fresh.csv','utf-8')

const json = csvJSON(data)

console.log(json)

function csvJSON(csv: any){

  var lines=csv.split("\n");

  var result = [];

  // NOTE: If your columns contain commas in their values, you'll need
  // to deal with those before doing the next step 
  // (you might convert them to &&& or something, then covert them back later)
  // jsfiddle showing the issue https://jsfiddle.net/
  var headers=lines[0].split(",");

  for(var i=1;i<lines.length;i++){

      var obj = {} as any;
      var currentline=lines[i].split(",");

      for(var j=0;j<headers.length;j++){
          obj[headers[j] as any] = currentline[j] as any;
      }

      result.push(obj);

  }
  //return result; //JavaScript object
  return JSON.stringify(result); //JSON
}
