import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { logsApi } from '../../api/endpoints/index';
import { CapabilityUnavailable } from '../../components/ui/CapabilityUnavailable';
import { EngineeringPanel, PanelBody, Button, DataTable, type Column } from '../../design-system/components';
import { formatBandId, formatCount } from '../../utils/formatters';
import type { LogEntry } from '../../types/api';
import { useSimulationStore } from '../../stores/simulation';

const CATEGORIES = ['', 'SIMULATION', 'DETECTION', 'SYSTEM'] as const;
const EMPTY_LOGS: any[] = [];

export default function LogsPage() {
  const [category, setCategory] = useState('');
  const [limit, setLimit] = useState(200);

  const { data: logs, isLoading, refetch } = useQuery({
    queryKey: ['logs', category, limit],
    queryFn:  () => logsApi.list({ category: category || undefined, limit }),
    refetchInterval: 3000,
  });

  const liveLogs = useSimulationStore((s) => s.recentTicks[s.recentTicks.length - 1]?.logs) || EMPTY_LOGS;

  const columns: Column<LogEntry>[] = [
    {
      key: 'time',
      header: 'Time',
      isMono: true,
      render: (l) => (l.time != null ? `t=${l.time}` : '—'),
    },
    {
      key: 'category',
      header: 'Category',
      render: (l) => (
        <span
          style={{
            fontSize: '11px',
            fontWeight: 600,
            textTransform: 'uppercase',
            color:
              l.category === 'DETECTION'
                ? 'var(--color-rf-blue)'
                : l.category === 'SYSTEM'
                ? 'var(--color-warning)'
                : 'var(--color-text-muted)',
          }}
        >
          {l.category}
        </span>
      ),
    },
    {
      key: 'type',
      header: 'Event Type',
      render: (l) => <span style={{ fontSize: '11px', color: 'var(--color-text-muted)', fontFamily: 'var(--font-mono)' }}>{l.type ?? '—'}</span>,
    },
    {
      key: 'band',
      header: 'Band',
      isMono: true,
      render: (l) => formatBandId(l.band_id),
    },
    {
      key: 'outcome',
      header: 'Outcome',
      render: (l) => (
        <span
          style={{
            fontWeight: 600,
            fontSize: '11px',
            color:
              l.outcome === 'HIT'
                ? 'var(--color-success)'
                : l.outcome === 'MISS'
                ? 'var(--color-text-muted)'
                : l.outcome === 'FALSE_ALARM'
                ? 'var(--color-warning)'
                : undefined,
          }}
        >
          {l.outcome ?? '—'}
        </span>
      ),
    },
    {
      key: 'message',
      header: 'Message Details',
      render: (l) => <span style={{ fontSize: '12px', color: 'var(--color-text-primary)' }}>{l.message}</span>,
    },
  ];

  const historicalLogs: LogEntry[] = Array.isArray(logs?.logs) ? logs.logs.slice().reverse() : [];
  
  // Transform live logs (which are lightweight) to LogEntry format for the table
  const formattedLiveLogs = liveLogs.map(l => ({
    time: l.time,
    category: l.category as any,
    message: l.message,
    type: null,
    band_id: null,
    outcome: null
  }));

  const logEntries: LogEntry[] = [...formattedLiveLogs.reverse(), ...historicalLogs];

  return (
    <div style={{ padding: 'var(--space-6)', display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 style={{ fontSize: '24px', fontWeight: 600, color: 'var(--color-primary-navy)', margin: '0 0 var(--space-2) 0' }}>
            System &amp; Simulation Logs
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-muted)', margin: 0 }}>
            Structured runtime audit log — filter by subsystem, inspect error events, and export raw logs
          </p>
        </div>
        <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
          <a href={logsApi.exportUrl('json')} target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
            <Button variant="secondary" size="compact">Export JSON</Button>
          </a>
          <a href={logsApi.exportUrl('csv')} target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
            <Button variant="secondary" size="compact">Export CSV</Button>
          </a>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
        <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>Subsystem</span>
        {CATEGORIES.map((c) => (
          <Button
            key={c || 'all'}
            size="compact"
            variant={category === c ? 'primary' : 'secondary'}
            onClick={() => setCategory(c)}
          >
            {c || 'All Subsystems'}
          </Button>
        ))}
        <div style={{ width: '1px', height: '16px', background: 'var(--color-border)', margin: '0 var(--space-2)' }} />
        
        <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', textTransform: 'uppercase' }}>Display Limit</span>
        <select 
          value={limit} 
          onChange={(e) => setLimit(Number(e.target.value))}
          style={{ height: 26, border: '1px solid var(--color-border)', borderRadius: 'var(--radius-sm)', padding: '0 var(--space-2)', fontSize: '12px', background: 'var(--color-surface-primary)', color: 'var(--color-text-primary)' }}
        >
          <option value={100}>100 rows</option>
          <option value={200}>200 rows</option>
          <option value={500}>500 rows</option>
          <option value={1000}>1000 rows</option>
        </select>
        <Button variant="secondary" size="compact" onClick={() => refetch()}>
          ↻ Refresh
        </Button>
        {logs && (
          <span style={{ fontSize: '12px', color: 'var(--color-text-muted)', marginLeft: 'auto' }}>
            {formatCount(logs.total ?? logEntries.length)} entries
          </span>
        )}
      </div>

      {!isLoading && !logs?.available ? (
        <CapabilityUnavailable title="No Log Telemetry" detail={logs?.detail ?? 'Start a simulation to generate structured runtime logs.'} />
      ) : (
        <EngineeringPanel>
          <PanelBody style={{ padding: 0, overflowX: 'auto', maxHeight: '65vh' }}>
            <DataTable 
              data={logEntries} 
              columns={columns} 
              rowKey={(l, i) => `${l.time}-${l.category}-${l.type}-${i}`} 
              loading={isLoading && !logs}
              emptyMessage="No log records match the selected subsystem criteria."
            />
          </PanelBody>
        </EngineeringPanel>
      )}
    </div>
  );
}
