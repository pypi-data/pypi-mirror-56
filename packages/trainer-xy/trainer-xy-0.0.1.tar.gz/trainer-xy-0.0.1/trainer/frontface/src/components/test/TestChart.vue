<template>
  <div id="main" style="width: 600px;height: 400px;"></div>
</template>
<script>
import echarts from "echarts";

export default {
  name: "TestChart",
  data() {
    return {
      charts: ""
    };
  },
  methods: {
    initLine(id) {
      this.charts = echarts.init(document.getElementById(id));
      this.charts.setOption({
        title: {
          text: "",// "动态数据 + 时间坐标轴"
        },
        tooltip: {
          trigger: "axis",
          formatter: function(params) {
            params = params[0];
            return params.value[0] + " : " + params.value[1];
          },
          axisPointer: {
            animation: false
          }
        },
        xAxis: {
          type: "time",
          splitLine: {
            show: false
          }
        },
        yAxis: {
          type: "value",
          boundaryGap: [0, "100%"],
          splitLine: {
            show: false
          }
        },
        animation: false
      });
    }
  },
  mounted() {
    this.$nextTick(function() {
      this.initLine("main");
      this.charts.setOption({
        series: [
          {
            name: "模拟数据0",
            type: "line",
            showSymbol: false,
            hoverAnimation: false,
            data: [["2018-01-02", "3"], ["2018-01-05", "4"]]
          }
        ]
      });

      setTimeout(() => {
        this.charts.appendData({
          seriesIndex: 0,
          data: [["2018-01-03", "1"], ["2018-01-07", "2"]]
        });
      }, 2000);

      setTimeout(() => {
        this.charts.resize();
      }, 4000);

      setTimeout(() => {
        this.charts.setOption({
          series: [
            {},
            {
              name: "模拟数据1",
              type: "line",
              showSymbol: false,
              hoverAnimation: false,
              data: [["2018-01-02", "5"], ["2018-01-05", "10"]]
            }
          ]
        });
        this.charts.appendData({
          seriesIndex: 1,
          data: [["2018-01-03", "11"], ["2018-01-10", "2"]]
        });
      }, 6000);
      setTimeout(() => {
        this.charts.resize();
      }, 8000);
    });
  }
};
</script>
<style scoped>
</style>
