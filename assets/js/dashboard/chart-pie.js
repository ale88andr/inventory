var usedEquipments = $('#eq-used').text();
var unusedEquipments = $('#eq-unused').text();
var repairedEquipments = $('#eq-repair').text();
var wInvEquipments = $('#eq-w-inv').text();

var dataSource = [
    { category: "Используется<br/>оборудования (" + usedEquipments + ")", number: parseInt(usedEquipments) },
    { category: "Не используется<br/>оборудования (" + unusedEquipments + ")", number: parseInt(unusedEquipments) },
    { category: "Находится в ремонте (" + repairedEquipments + ")", number: parseInt(repairedEquipments) },
    { category: "Оборудывание<br/>без инвентарного (" + wInvEquipments + ")", number: parseInt(wInvEquipments) }
];

$("#chartContainer").dxPieChart({
    dataSource: dataSource,
    title: "Использование <br>",
    series: {
        type: "donut",
        argumentField: "category",
        valueField: "number",
        innerRadius: 0.5,
        hoverMode: "none"
    },
    legend: {
        verticalAlignment: "bottom",
        horizontalAlignment: "center",
        equalColumnWidth: true
    },
    tooltip: {
        enabled: true,
        customizeText: function () {
            return this.argumentText + "<br/>"
            + this.percentText + " (" + this.valueText + ")";
        }
    }
});