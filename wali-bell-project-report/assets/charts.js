(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  // --- Chart 1: Question Type Distribution (Pie) ---
  var chart1 = echarts.init(document.getElementById('chart-question-type'), null, { renderer: 'svg' });
  chart1.setOption({
    animation: false,
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} 题 ({d}%)',
      appendToBody: true
    },
    legend: {
      bottom: 10,
      left: 'center',
      textStyle: { color: muted, fontSize: 13 }
    },
    series: [{
      name: '题型配比',
      type: 'pie',
      radius: ['40%', '65%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 8,
        borderColor: bg2,
        borderWidth: 3
      },
      label: {
        show: true,
        formatter: '{b}\n{c} 题',
        color: ink,
        fontSize: 14,
        fontWeight: 600
      },
      labelLine: { show: true },
      data: [
        { value: 15, name: '选择题', itemStyle: { color: accent } },
        { value: 10, name: '判断题', itemStyle: { color: accent2 } },
        { value: 2, name: '编程大题', itemStyle: { color: '#8b5cf6' } }
      ]
    }]
  });
  window.addEventListener('resize', function() { chart1.resize(); });

  // --- Chart 2: Module Completion (Bar) ---
  var chart2 = echarts.init(document.getElementById('chart-completion'), null, { renderer: 'svg' });
  chart2.setOption({
    animation: false,
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: function(params) {
        return params[0].name + ': ' + params[0].value + '%';
      },
      appendToBody: true
    },
    grid: {
      left: '3%',
      right: '8%',
      bottom: '3%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      max: 100,
      axisLabel: { color: muted, fontSize: 12, formatter: '{value}%' },
      axisLine: { lineStyle: { color: rule } },
      splitLine: { lineStyle: { color: rule, type: 'dashed' } }
    },
    yAxis: {
      type: 'category',
      data: [
        '端到端联调测试',
        '前端页面',
        'OJ 判题系统',
        '老师端资料管理',
        '诊断闭环',
        '数据库设计',
        '后端 API',
        '题库数据',
        '智能抽题+复测',
        '反作弊机制'
      ],
      axisLabel: { color: ink, fontSize: 12 },
      axisLine: { lineStyle: { color: rule } },
      axisTick: { show: false }
    },
    series: [{
      name: '完成度',
      type: 'bar',
      data: [
        { value: 40, itemStyle: { color: muted } },
        { value: 85, itemStyle: { color: accent } },
        { value: 85, itemStyle: { color: accent } },
        { value: 90, itemStyle: { color: accent2 } },
        { value: 95, itemStyle: { color: accent2 } },
        { value: 100, itemStyle: { color: accent2 } },
        { value: 100, itemStyle: { color: accent2 } },
        { value: 100, itemStyle: { color: accent2 } },
        { value: 100, itemStyle: { color: accent2 } },
        { value: 100, itemStyle: { color: accent2 } }
      ],
      barWidth: '55%',
      label: {
        show: true,
        position: 'right',
        formatter: '{c}%',
        color: ink,
        fontSize: 12,
        fontWeight: 600
      },
      itemStyle: { borderRadius: [0, 6, 6, 0] }
    }]
  });
  window.addEventListener('resize', function() { chart2.resize(); });
})();
