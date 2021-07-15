(function($) {
    'use strict';

    am4core.ready(function() {

        window.am4themes_edenConception = function (target) {
            if (target instanceof am4core.ColorSet) {
                target.list = [
                    am4core.color("#283250"),
                    am4core.color("#70e5cd"),
                    am4core.color("#902c2d"),
                    am4core.color("#d5433d"),
                    am4core.color("#f05440"),
                ];
            }

            if (target instanceof am4core.InterfaceColorSet) {
                target.setFor("text", am4core.color("#dbdada"));
                target.setFor("grid", am4core.color("#dbdada"));
              }
        }

        window.get_stats = function (datas, projectId) {
            am4core.useTheme(am4themes_edenConception);
            am4core.useTheme(am4themes_animated);

            // Create chart instance
            let htmlElement = 'project-nb-task-by-list-' + projectId
            var chart = am4core.create(htmlElement, am4charts.PieChart);

            // Add and configure Series
            var pieSeries = chart.series.push(new am4charts.PieSeries());
            pieSeries.dataFields.category = "list";
            pieSeries.dataFields.value = "nb_task";

            // Let's cut a hole in our Pie chart the size of 30% the radius
            chart.innerRadius = am4core.percent(30);

            // Put a thick white border around each Slice
            pieSeries.slices.template.stroke = am4core.color("#fff");
            pieSeries.slices.template.strokeWidth = 2;
            pieSeries.slices.template.strokeOpacity = 1;
            pieSeries.slices.template
            // change the cursor on hover to make it apparent the object can be interacted with
            .cursorOverStyle = [
                {
                "property": "cursor",
                "value": "pointer"
                }
            ];
 
            pieSeries.labels.template.disabled = true;
            pieSeries.ticks.template.disabled = true;

            // Create a base filter effect (as if it's not there) for the hover to return to
            var shadow = pieSeries.slices.template.filters.push(new am4core.DropShadowFilter);
            shadow.opacity = 0;

            // Create hover state
            var hoverState = pieSeries.slices.template.states.getKey("hover"); // normally we have to create the hover state, in this case it already exists

            // Slightly shift the shadow and make it more prominent on hover
            var hoverShadow = hoverState.filters.push(new am4core.DropShadowFilter);
            hoverShadow.opacity = 0.7;
            hoverShadow.blur = 5;

            // Add a legend
            chart.legend = new am4charts.Legend();

            chart.data = datas
        }

        window.get_time = function (datas, projectId) {
            am4core.useTheme(am4themes_edenConception);
            am4core.useTheme(am4themes_animated);
        
            let htmlElement = 'project-planned-hour-' + projectId
            var chart = am4core.create(htmlElement, am4charts.XYChart)
            chart.colors.step = 2;
            
            chart.legend = new am4charts.Legend()
            chart.legend.position = 'top'
            chart.legend.paddingBottom = 20
            chart.legend.labels.template.maxWidth = 95
            
            var xAxis = chart.xAxes.push(new am4charts.CategoryAxis())
            xAxis.dataFields.category = 'list'
            xAxis.renderer.cellStartLocation = 0.1
            xAxis.renderer.cellEndLocation = 0.9
            xAxis.renderer.grid.template.location = 0;
            
            var yAxis = chart.yAxes.push(new am4charts.ValueAxis());
            yAxis.min = 0;
            
            function createSeries(value, name) {
                var series = chart.series.push(new am4charts.ColumnSeries())
                series.dataFields.valueY = value
                series.dataFields.categoryX = 'list'
                series.name = name
            
                series.events.on("hidden", arrangeColumns);
                series.events.on("shown", arrangeColumns);
            
                var bullet = series.bullets.push(new am4charts.LabelBullet())
                bullet.interactionsEnabled = false
                bullet.dy = 30;
                bullet.label.text = '{valueY}'
                bullet.label.fill = am4core.color('#ffffff')
            
                return series;
            }

            chart.data = datas

            createSeries('planned_hours', 'Planned hours');
            createSeries('effective_hours', 'Effective hours');
            
            function arrangeColumns() {
            
                var series = chart.series.getIndex(0);
            
                var w = 1 - xAxis.renderer.cellStartLocation - (1 - xAxis.renderer.cellEndLocation);
                if (series.dataItems.length > 1) {
                    var x0 = xAxis.getX(series.dataItems.getIndex(0), "categoryX");
                    var x1 = xAxis.getX(series.dataItems.getIndex(1), "categoryX");
                    var delta = ((x1 - x0) / chart.series.length) * w;
                    if (am4core.isNumber(delta)) {
                        var middle = chart.series.length / 2;
            
                        var newIndex = 0;
                        chart.series.each(function(series) {
                            if (!series.isHidden && !series.isHiding) {
                                series.dummyData = newIndex;
                                newIndex++;
                            }
                            else {
                                series.dummyData = chart.series.indexOf(series);
                            }
                        })
                        var visibleCount = newIndex;
                        var newMiddle = visibleCount / 2;
            
                        chart.series.each(function(series) {
                            var trueIndex = chart.series.indexOf(series);
                            var newIndex = series.dummyData;
            
                            var dx = (newIndex - trueIndex + middle - newMiddle) * delta
            
                            series.animate({ property: "dx", to: dx }, series.interpolationDuration, series.interpolationEasing);
                            series.bulletsContainer.animate({ property: "dx", to: dx }, series.interpolationDuration, series.interpolationEasing);
                        })
                    }
                }
            }
        }
    });
})(jQuery);
