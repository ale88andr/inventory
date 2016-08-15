var trDomElements = $(".types-annotation");

var dataSource = [];

trDomElements.each(function(key, item){
    var typeName = $(item).find('.type-name').text();
    var typeQuantity = $(item).find('.type-quantity').text();
    dataSource[key] = {'type': typeName, 'number': parseInt(typeQuantity)};
});

var showType = function (point) {
    var $catInfo = $("#catInfo"),
        $chartContainer = $("#chartContainerTypes"),
        offset = $chartContainer.offset();
    point.select();

    $("#typeName").html(point.argument);
    $("#typeNumber").text('(' + point.value + ')');
    $catInfo.show();
};

$("#chartContainerTypes").dxChart({
    dataSource: dataSource,
    title: "Типы оборудования",
    series: {
        name: "Типы",
        type: "bar",
        argumentField: "type",
        valueField: "number",
        hoverStyle: {
            hatching: "right"
        }
    },
    legend: { visible: false },
    pointHover: showType,
    pointClick: showType
});