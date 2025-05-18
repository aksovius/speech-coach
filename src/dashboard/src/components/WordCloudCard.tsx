'use client';

import { useEffect, useState, useRef } from 'react';
import * as d3 from 'd3';
import cloud from 'd3-cloud';

interface Word {
  text: string;
  value: number;
  size?: number;
  x?: number;
  y?: number;
  rotate?: number;
}

// Dummy data for demonstration
const dummyWords: Word[] = [
  { text: 'hello', value: 100 },
  { text: 'world', value: 80 },
  { text: 'speech', value: 90 },
  { text: 'practice', value: 85 },
  { text: 'language', value: 75 },
  { text: 'learning', value: 70 },
  { text: 'pronunciation', value: 65 },
  { text: 'fluency', value: 60 },
  { text: 'vocabulary', value: 55 },
  { text: 'communication', value: 50 },
  { text: 'confidence', value: 45 },
  { text: 'improvement', value: 40 },
  { text: 'progress', value: 35 },
  { text: 'skills', value: 30 },
  { text: 'development', value: 25 },
];

const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#0088fe'];

export default function WordCloudCard() {
  const [isMounted, setIsMounted] = useState(false);
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (!isMounted || !svgRef.current) return;

    const width = svgRef.current.clientWidth;
    const height = 300;

    // Clear previous content
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    const layout = cloud()
      .size([width, height])
      .words(dummyWords.map(d => ({
        text: d.text,
        size: 10 + (d.value / 2),
        value: d.value
      })))
      .padding(5)
      .rotate(() => ~~(Math.random() * 2) * 90)
      .font('Impact')
      .fontSize((d: any) => d.size || 10)
      .on('end', draw);

    layout.start();

    function draw(words: Word[]) {
      svg.append('g')
        .attr('transform', `translate(${width / 2},${height / 2})`)
        .selectAll('text')
        .data(words)
        .enter()
        .append('text')
        .style('font-size', d => `${d.size || 10}px`)
        .style('font-family', 'Impact')
        .style('fill', (_, i) => colors[i % colors.length])
        .attr('text-anchor', 'middle')
        .attr('transform', d => `translate(${d.x || 0},${d.y || 0}) rotate(${d.rotate || 0})`)
        .text(d => d.text);
    }
  }, [isMounted]);

  if (!isMounted) {
    return (
      <div className="rounded-lg bg-white p-4 shadow-sm">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Active Vocabulary</h2>
        <div className="h-[300px] w-full flex items-center justify-center text-gray-500">
          Loading...
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-900 mb-2">Active Vocabulary This Month</h2>
      <div className="h-[300px] w-full">
        <svg ref={svgRef} className="w-full h-full"></svg>
      </div>
    </div>
  );
}
