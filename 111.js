// ==UserScript==
// @name         auto search falcon
// @namespace    https://github.com/chenzf666/Weibo_1.0/blob/master/111.js
// @version      1.0.2
// @description  just demo !!!
// @author       chenzhifeng
// @match        https://monitorvpc.inkept.cn/*
// @icon         https://github.githubassets.com/favicons/favicon.png
// @updateURL    https://github.com/chenzf666/Weibo_1.0/blob/master/111.js
// @grant        none
// ==/UserScript==

const demo = '[P0][Ok][tx4-inno-sm-msg01.bj][][soulmatch.user.messagelogic服务自身接口可用性下降 all(#3) event.code.rate code=0,event=RestServe.api.v2.message.read,namespace=sm,project=sm.soulmatch.user.messagelogic 100<=99][O1 2021-12-05 21:39:00]'

const regFullText = /^\[P[0-3]\]\[(OK|PROBLEM)\]\[[a-z0-9\-.]+\]\[\]\[.+\]\[O\d\s[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])\s+(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d\]$/gi
const regEndpoint = /(-[a-z]+){3}/i
const regFilter = /event=[a-z0-g.,]+/i

function getEndpoints(endpoint, filter) {
    document.getElementById('endpoint-search').value = endpoint
    document.getElementById('counter-search').value = filter
    document.getElementById('btn-search-endpoints').click()
    const checkBtn = document.getElementById('check_all_endpoints')
    if (!checkBtn.checked) {
        checkBtn.click()
        console.log('click checkbox OK!');
    }
}

function searchCounters(endpoint) {
    let timer = window.setInterval(function () {
        let tb = document.getElementById('tbody-endpoints')
        if (tb.rows.length > 0 && tb.rows[0].cells[1].innerText.indexOf(endpoint) !== -1) {
            document.getElementById('counters').getElementsByClassName('btn-success').item(0).click()
            // window.fn_list_counters()
            console.log('search counters OK!');
            clearInterval(timer)
            filterCounters()
        }
    }, 100)
    setTimeout(() => {
        clearInterval(timer)
    }, 3000)
}

function filterCounters() {
    let timer = window.setInterval(function () {
        let tb = document.getElementById('tbody-counters')
        if (tb.rows.length > 0) {
            // let ct = tb.rows[0].cells[0].getElementsByClassName('shiftCheckbox')[0].getAttribute('data-fullkey')
            // if (ct.indexOf('event.code.count') === -1) {
            // 快速过滤
            document.getElementById('counter-filter').value = 'event.code.count'
            document.getElementById('counters').getElementsByClassName('btn-info').item(0).click()
            // window.filter_counter()
            console.log('filter counters OK!');
            clearInterval(timer)
            // }
        }
    }, 100)
    setTimeout(() => {
        clearInterval(timer)
    }, 3000)
}

window.onload = async function () {
    await navigator.clipboard.readText().then(text => {
        // text = demo
        if (!regFullText.test(text)) {
            return
        }
        let endpoint = text.match(regEndpoint)[0]
        let filter = text.match(regFilter)[0]
        if (endpoint === '' || filter === '') {
            return;
        }
        getEndpoints(endpoint, filter)
        searchCounters(endpoint)
    })
}
