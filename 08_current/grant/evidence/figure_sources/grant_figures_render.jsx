/**
 * EPSRC JeS figure — schematic + 12-month workplan.
 *
 * Print from grant_figure.html at full text width (~16 cm).
 * Month numbers locked to TIMELINE.md / 02_Vision_and_Approach.md.
 * Compact timeline-only export: grant_figure_gantt.svg (JeS Figure 1).
 *
 * Caption (combined):
 * Figure 1. (a) Schematic. At a single threshold δ both configurations have
 * two connected components, so a count cannot tell them apart. Their
 * persistence profiles differ: spread rings support longer H₁ bars than
 * compact clusters, and the Wasserstein distance W₁(A, B) is large.
 * Orange: H₀ (components); blue: H₁ (loops). (b) Twelve-month workplan (§4).
 * Diamonds: decision milestones. Triangles: outputs. Research Associate in
 * post Months 2–10.
 */
export default function GrantFigures() {
  const dark = '#1C2B40', blue = '#2A5FA5', green = '#2E7D52', orange = '#C4611E';
  const purple = '#5B3FA0', red = '#B03A2E', grid = '#DDE3EC', bg = '#F4F7FB';
  const bord = '#B8C5D6', muted = '#6B7C93';
  const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

  const CL = 168, MW = 40;
  const mc = n => CL + (n - 0.5) * MW;
  const ml = n => CL + (n - 1) * MW;
  const bx = s => ml(s);
  const bw = (s, e) => (e - s + 1) * MW;
  const dia = (cx, cy, r = 8) =>
    `M${cx},${cy - r} L${cx + r * 0.82},${cy} L${cx},${cy + r} L${cx - r * 0.82},${cy} Z`;
  const tri = (cx, cy, r = 7) =>
    `M${cx},${cy - r} L${cx + r},${cy + r * 0.85} L${cx - r},${cy + r * 0.85} Z`;

  const ringA = [
    [58, 90], [73, 97], [80, 112], [73, 127], [58, 134], [43, 127], [36, 112], [43, 97],
  ];
  const ringA2 = ringA.map(([x, y]) => [x + 84, y]);
  const blobB = [
    [253, 104], [263, 103], [268, 111], [264, 120],
    [254, 121], [248, 114], [258, 112], [258, 128],
  ];
  const blobB2 = blobB.map(([x, y]) => [x + 84, y]);
  const barsA = [[140, orange, 0.90], [136, orange, 0.90], [92, orange, 0.60], [80, orange, 0.60], [58, blue, 0.85], [44, blue, 0.85], [30, blue, 0.85]];
  const barsB = [[140, orange, 0.90], [136, orange, 0.90], [16, orange, 0.50], [12, orange, 0.50], [10, blue, 0.50], [8, blue, 0.50], [6, blue, 0.50]];

  return (
    <div style={{display: 'flex', width: 1080, height: 500, background: 'white', fontFamily: font, border: `1px solid ${bord}`, borderRadius: 4, overflow: 'hidden'}}>
      <div style={{width: 400, flexShrink: 0, borderRight: `1px solid ${bord}`, boxSizing: 'border-box'}}>
        <svg viewBox="0 0 400 500" width={400} height={500}>
          <text x={8} y={22} fontSize={16} fontWeight={700} fill={dark}>(a)</text>
          <text x={200} y={22} textAnchor="middle" fontSize={14} fill={muted} fontStyle="italic">Single-scale counts cannot distinguish</text>
          <text x={100} y={46} textAnchor="middle" fontSize={14} fontWeight={700} fill={dark}>A  ·  spread rings</text>
          <text x={300} y={46} textAnchor="middle" fontSize={14} fontWeight={700} fill={dark}>B  ·  compact clusters</text>

          <rect x={16} y={54} width={168} height={118} rx={3} fill={bg} stroke={bord}/>
          <rect x={216} y={54} width={168} height={118} rx={3} fill={bg} stroke={bord}/>

          <circle cx={58} cy={112} r={32} fill="rgba(42,95,165,0.07)" stroke={blue} strokeWidth={1.1} strokeDasharray="3.5 2.5"/>
          <circle cx={142} cy={112} r={32} fill="rgba(42,95,165,0.07)" stroke={blue} strokeWidth={1.1} strokeDasharray="3.5 2.5"/>
          <polygon points="58,90 73,97 80,112 73,127 58,134 43,127 36,112 43,97" fill="none" stroke={orange} strokeWidth={1.1} opacity={0.85}/>
          <polygon points="142,90 157,97 164,112 157,127 142,134 127,127 120,112 127,97" fill="none" stroke={orange} strokeWidth={1.1} opacity={0.85}/>
          {ringA.map(([cx, cy], i) => <circle key={`a1${i}`} cx={cx} cy={cy} r={3.4} fill={dark}/>)}
          {ringA2.map(([cx, cy], i) => <circle key={`a2${i}`} cx={cx} cy={cy} r={3.4} fill={dark}/>)}

          <text x={200} y={122} textAnchor="middle" fontSize={26} fontWeight={700} fill={green}>=</text>

          <circle cx={258} cy={112} r={22} fill="rgba(42,95,165,0.07)" stroke={blue} strokeWidth={1.1} strokeDasharray="3.5 2.5"/>
          <circle cx={342} cy={112} r={22} fill="rgba(42,95,165,0.07)" stroke={blue} strokeWidth={1.1} strokeDasharray="3.5 2.5"/>
          <ellipse cx={258} cy={112} rx={11} ry={13} fill={dark} opacity={0.08}/>
          <ellipse cx={342} cy={112} rx={11} ry={13} fill={dark} opacity={0.08}/>
          {blobB.map(([cx, cy], i) => <circle key={`b1${i}`} cx={cx} cy={cy} r={3.2} fill={dark}/>)}
          {blobB2.map(([cx, cy], i) => <circle key={`b2${i}`} cx={cx} cy={cy} r={3.2} fill={dark}/>)}

          <text x={100} y={190} textAnchor="middle" fontSize={14} fontWeight={700} fill={blue}>H₀ = 2 at δ</text>
          <text x={300} y={190} textAnchor="middle" fontSize={14} fontWeight={700} fill={blue}>H₀ = 2 at δ</text>
          <text x={200} y={210} textAnchor="middle" fontSize={13} fill={muted} fontStyle="italic">Identical at one threshold</text>

          <line x1={16} y1={222} x2={384} y2={222} stroke={grid}/>
          <text x={200} y={242} textAnchor="middle" fontSize={13} fill={muted} fontStyle="italic">Persistence profile across scales</text>

          <rect x={16} y={252} width={168} height={150} rx={3} fill={bg} stroke={bord}/>
          <rect x={216} y={252} width={168} height={150} rx={3} fill={bg} stroke={bord}/>
          {barsA.map(([w, col, op], i) => <rect key={`ba${i}`} x={28} y={266 + i * 16} width={w} height={9} rx={1.5} fill={col} opacity={op}/>)}
          {barsB.map(([w, col, op], i) => <rect key={`bb${i}`} x={228} y={266 + i * 16} width={w} height={9} rx={1.5} fill={col} opacity={op}/>)}
          <line x1={168} y1={262} x2={168} y2={378} stroke={blue} strokeWidth={1} strokeDasharray="3 2"/>
          <line x1={368} y1={262} x2={368} y2={378} stroke={blue} strokeWidth={1} strokeDasharray="3 2"/>
          <line x1={28} y1={380} x2={168} y2={380} stroke="#8895A7"/>
          <line x1={228} y1={380} x2={368} y2={380} stroke="#8895A7"/>
          <text x={28} y={394} fontSize={12} fill="#8895A7">0</text>
          <text x={168} y={394} textAnchor="end" fontSize={12} fill="#8895A7">δ</text>
          <text x={228} y={394} fontSize={12} fill="#8895A7">0</text>
          <text x={368} y={394} textAnchor="end" fontSize={12} fill="#8895A7">δ</text>
          <text x={200} y={338} textAnchor="middle" fontSize={26} fontWeight={700} fill={red}>≠</text>

          <rect x={16} y={412} width={16} height={8} rx={1.5} fill={orange} opacity={0.9}/>
          <text x={38} y={420} fontSize={13} fill={dark}>H₀  components</text>
          <rect x={196} y={412} width={16} height={8} rx={1.5} fill={blue} opacity={0.85}/>
          <text x={218} y={420} fontSize={13} fill={dark}>H₁  loops</text>
          <text x={200} y={448} textAnchor="middle" fontSize={13} fill={muted} fontStyle="italic">Same H₀ count — different internal structure</text>
          <text x={200} y={476} textAnchor="middle" fontSize={16} fontWeight={700} fill={red}>W₁(A, B) ≫ 0</text>
          <text x={200} y={494} textAnchor="middle" fontSize={12} fill={muted}>Wasserstein distance between profiles</text>
        </svg>
      </div>

      <div style={{flex: 1, boxSizing: 'border-box'}}>
        <svg viewBox="0 0 672 500" width="100%" height="100%">
          <text x={8} y={22} fontSize={16} fontWeight={700} fill={dark}>(b)</text>
          <text x={340} y={22} textAnchor="middle" fontSize={14} fill={muted} fontStyle="italic">Twelve-month workplan</text>

          <rect x={CL} y={32} width={12 * MW} height={22} rx={2} fill="#EEF2F7"/>
          <text x={CL - 8} y={48} textAnchor="end" fontSize={13} fill={muted}>Month</text>
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(n => (
            <text key={n} x={mc(n)} y={48} textAnchor="middle" fontSize={13} fill="#4A5568">{n}</text>
          ))}
          {[...Array(13)].map((_, i) => (
            <line key={i} x1={ml(i + 1)} y1={56} x2={ml(i + 1)} y2={292} stroke={grid} strokeWidth={0.7}/>
          ))}

          <text x={CL - 8} y={74} textAnchor="end" fontSize={12} fill={muted} fontStyle="italic">Team</text>
          <text x={CL - 8} y={94} textAnchor="end" fontSize={13} fill={dark}>PI  (0.2 FTE)</text>
          <rect x={bx(1)} y={82} width={bw(1, 12)} height={14} rx={2} fill={dark} fillOpacity={0.16} stroke={dark} strokeOpacity={0.35}/>
          <text x={CL - 8} y={116} textAnchor="end" fontSize={13} fill={dark}>Co-Is  (0.1)</text>
          <rect x={bx(1)} y={104} width={bw(1, 12)} height={14} rx={2} fill={purple} fillOpacity={0.18} stroke={purple} strokeOpacity={0.3}/>
          <text x={CL - 8} y={138} textAnchor="end" fontSize={13} fill={dark}>Res. Associate</text>
          <rect x={bx(2)} y={126} width={bw(2, 10)} height={14} rx={2} fill={blue} opacity={0.78}/>

          <line x1={8} y1={152} x2={660} y2={152} stroke={bord}/>
          <text x={CL - 8} y={170} textAnchor="end" fontSize={12} fill={muted} fontStyle="italic">Objectives</text>
          <text x={CL - 8} y={190} textAnchor="end" fontSize={13} fill={dark}>O1  Geometry</text>
          <rect x={bx(1)} y={178} width={bw(1, 9)} height={14} rx={2} fill={green} opacity={0.78}/>
          <text x={CL - 8} y={214} textAnchor="end" fontSize={13} fill={dark}>O2  Inference</text>
          <rect x={bx(4)} y={202} width={bw(4, 10)} height={14} rx={2} fill={orange} opacity={0.78}/>

          <line x1={8} y1={228} x2={660} y2={228} stroke={bord}/>
          <text x={CL - 8} y={246} textAnchor="end" fontSize={12} fill={muted} fontStyle="italic">Milestones</text>
          {[[2, '1'], [7, '2'], [8, '3'], [9, '4']].map(([n, lbl]) => (
            <g key={`m${n}`}>
              <text x={mc(n)} y={246} textAnchor="middle" fontSize={13} fill={dark}>{lbl}</text>
              <path d={dia(mc(n), 262, 8)} fill={dark}/>
            </g>
          ))}

          <line x1={8} y1={280} x2={660} y2={280} stroke={bord}/>
          <text x={CL - 8} y={298} textAnchor="end" fontSize={12} fill={muted} fontStyle="italic">Outputs</text>
          {[[2, '[17]'], [10, 'Handover'], [11, 'Paper'], [12, 'Pack']].map(([n, lbl]) => (
            <g key={`o${n}`}>
              <path d={tri(mc(n), 294, 7)} fill={purple}/>
              <text x={mc(n)} y={318} textAnchor="middle" fontSize={12} fill={purple}>{lbl}</text>
            </g>
          ))}

          <rect x={8} y={338} width={22} height={9} rx={2} fill={dark} fillOpacity={0.16} stroke={dark} strokeOpacity={0.35}/>
          <text x={36} y={347} fontSize={12} fill={dark}>PI M1–12</text>
          <rect x={118} y={338} width={22} height={9} rx={2} fill={purple} fillOpacity={0.18} stroke={purple} strokeOpacity={0.3}/>
          <text x={146} y={347} fontSize={12} fill={dark}>Co-Is 0.1 FTE</text>
          <rect x={268} y={338} width={22} height={9} rx={2} fill={blue} opacity={0.78}/>
          <text x={296} y={347} fontSize={12} fill={dark}>RA M2–10</text>
          <rect x={388} y={338} width={22} height={9} rx={2} fill={green} opacity={0.78}/>
          <text x={416} y={347} fontSize={12} fill={dark}>O1 M1–9</text>
          <rect x={500} y={338} width={22} height={9} rx={2} fill={orange} opacity={0.78}/>
          <text x={528} y={347} fontSize={12} fill={dark}>O2 M4–10</text>

          <path d={dia(16, 372, 6)} fill={dark}/>
          <text x={30} y={376} fontSize={12} fill={dark}>Decision milestone</text>
          <path d={tri(188, 370, 6)} fill={purple}/>
          <text x={204} y={376} fontSize={12} fill={dark}>Deliverable</text>

          <text x={8} y={408} fontSize={13} fill={dark}>1  Pre-registration and cutoff gate (M2)     2  Barcode archive and moment conditions (M7)</text>
          <text x={8} y={428} fontSize={13} fill={dark}>3  Landscape module (M8)     4  T1/T2, change-points and O1 geometry (M9)</text>
          <text x={8} y={456} fontSize={13} fill={purple}>▲  [17] submitted (M2)     RA handover (M10)</text>
          <text x={8} y={476} fontSize={13} fill={purple}>     Season paper (M11)     Evidence pack (M12)</text>
        </svg>
      </div>
    </div>
  );
}
