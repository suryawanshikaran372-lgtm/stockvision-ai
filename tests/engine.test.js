import test from 'node:test';import assert from 'node:assert/strict';import {parseCSV,analyze} from '../site/engine.js';
const header='year,revenue,profit,debt,equity,operating_cash_flow,capex,shares,source_url';const data=header+'\n2024,100,10,20,50,12,3,5,https://example.org/24\n2025,121,12,10,60,13,4,5,https://example.org/25';
test('valid financial calculations',()=>{const a=analyze(parseCSV(data),20);assert.equal(a.metrics.revenue_cagr_pct,21);assert.equal(a.metrics.profit_cagr_pct,20);assert.equal(a.metrics.debt_to_equity,.17);assert.equal(a.metrics.eps,2.4);assert.equal(a.metrics.pe,8.33);assert.equal(a.metrics.free_cash_flow,9);});
test('rejects duplicate years',()=>assert.throws(()=>analyze(parseCSV(data.replace('2025,','2024,'))),/Duplicate/));
test('rejects non-HTTPS sources',()=>assert.throws(()=>analyze(parseCSV(data.replace('https://example.org/25','javascript:alert(1)'))),/HTTPS/));
test('rejects invalid price',()=>assert.throws(()=>analyze(parseCSV(data),-1),/positive/));
test('quoted CSV values',()=>assert.equal(parseCSV(data.replace('https://example.org/25','"https://example.org/25"'))[1].year,'2025'));
