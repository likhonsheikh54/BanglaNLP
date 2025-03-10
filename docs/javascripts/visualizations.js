// Initialize D3.js visualizations
const initVisualization = () => {
    // Language Distribution Tree Map
    const treeMapData = {
        name: 'Dataset',
        children: [
            { name: 'News', value: 45000 },
            { name: 'Sports', value: 25000 },
            { name: 'Technology', value: 20000 },
            { name: 'Entertainment', value: 15000 },
            { name: 'Business', value: 10000 },
            { name: 'Others', value: 5000 }
        ]
    };

    const width = 800;
    const height = 400;

    const treemap = d3.treemap()
        .size([width, height])
        .padding(1);

    const root = d3.hierarchy(treeMapData)
        .sum(d => d.value);

    treemap(root);

    const svg = d3.select('#topic-distribution')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    const nodes = svg.selectAll('g')
        .data(root.leaves())
        .join('g')
        .attr('transform', d => `translate(${d.x0},${d.y0})`);

    nodes.append('rect')
        .attr('width', d => d.x1 - d.x0)
        .attr('height', d => d.y1 - d.y0)
        .attr('fill', (d, i) => d3.schemeSet3[i])
        .attr('opacity', 0)
        .transition()
        .duration(800)
        .attr('opacity', 1);

    nodes.append('text')
        .text(d => d.data.name)
        .attr('dx', 3)
        .attr('dy', 15)
        .attr('fill', 'white');
};

// Initialize ApexCharts
const initCharts = () => {
    const qualityMetrics = new ApexCharts(
        document.querySelector("#quality-metrics"),
        {
            series: [{
                data: [99.2, 92, 95.5, 97.8]
            }],
            chart: {
                type: 'bar',
                height: 350,
                animations: {
                    enabled: true,
                    easing: 'easeinout',
                    speed: 800
                }
            },
            xaxis: {
                categories: [
                    'Language Detection',
                    'Alignment Accuracy',
                    'Content Quality',
                    'Overall Score'
                ]
            }
        }
    );
    qualityMetrics.render();
};

document.addEventListener('DOMContentLoaded', () => {
    initVisualization();
    initCharts();
});
