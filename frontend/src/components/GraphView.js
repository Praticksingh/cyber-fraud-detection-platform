import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './GraphView.css';

function GraphView({ graphData, loading }) {
  const svgRef = useRef();

  useEffect(() => {
    if (!graphData || !graphData.nodes || graphData.nodes.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = svgRef.current.clientWidth;
    const height = 400;

    const g = svg.append('g');

    // Add zoom behavior
    const zoom = d3.zoom()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    // Create simulation
    const simulation = d3.forceSimulation(graphData.nodes)
      .force('link', d3.forceLink(graphData.edges).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(30));

    // Draw edges
    const link = g.append('g')
      .selectAll('line')
      .data(graphData.edges)
      .enter()
      .append('line')
      .attr('stroke', '#4a5568')
      .attr('stroke-width', d => Math.max(1, d.weight * 3))
      .attr('stroke-opacity', 0.6);

    // Draw nodes
    const node = g.append('g')
      .selectAll('circle')
      .data(graphData.nodes)
      .enter()
      .append('circle')
      .attr('r', d => Math.max(8, Math.min(20, d.incident_count * 3)))
      .attr('fill', d => {
        if (d.risk_score <= 30) return '#10b981';
        if (d.risk_score <= 70) return '#f59e0b';
        return '#ef4444';
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    // Add labels
    const label = g.append('g')
      .selectAll('text')
      .data(graphData.nodes)
      .enter()
      .append('text')
      .text(d => d.label)
      .attr('font-size', 10)
      .attr('fill', '#e0e0e0')
      .attr('text-anchor', 'middle')
      .attr('dy', -25);

    // Add tooltips
    node.append('title')
      .text(d => `${d.label}\nRisk: ${d.risk_score}\nIncidents: ${d.incident_count}`);

    // Update positions on tick
    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);

      label
        .attr('x', d => d.x)
        .attr('y', d => d.y);
    });

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [graphData]);

  if (loading) {
    return (
      <div className="chart-card">
        <h3 className="chart-title">Knowledge Graph</h3>
        <div className="chart-loading">
          <div className="loading-spinner"></div>
        </div>
      </div>
    );
  }

  if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
    return (
      <div className="chart-card">
        <h3 className="chart-title">Knowledge Graph</h3>
        <div className="graph-empty">
          <p>No graph data available yet. Analyze some messages to build the knowledge graph.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-card">
      <div className="graph-header">
        <h3 className="chart-title">Knowledge Graph</h3>
        <div className="graph-legend">
          <div className="legend-item">
            <span className="legend-dot" style={{ background: '#10b981' }}></span>
            <span>Low Risk (0-30)</span>
          </div>
          <div className="legend-item">
            <span className="legend-dot" style={{ background: '#f59e0b' }}></span>
            <span>Medium Risk (31-70)</span>
          </div>
          <div className="legend-item">
            <span className="legend-dot" style={{ background: '#ef4444' }}></span>
            <span>High Risk (71-100)</span>
          </div>
        </div>
      </div>
      <svg ref={svgRef} className="graph-svg"></svg>
      <div className="graph-info">
        <p>Drag nodes to explore • Scroll to zoom • {graphData.nodes.length} entities • {graphData.edges.length} connections</p>
      </div>
    </div>
  );
}

export default GraphView;
