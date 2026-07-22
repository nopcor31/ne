import React, { useState } from 'react';
import { Cotizacion, Cliente, ContactoCliente, EstadoCotizacion } from '../types';
import { KanbanBoard } from '../components/KanbanBoard';
import { StateBadge } from '../components/StateBadge';
import { ESTADO_LABELS } from '../services/stateMachine';
import { FileText, LayoutGrid, List, Plus, Building, DollarSign, Calendar, Eye } from 'lucide-react';

interface CotizacionesViewProps {
  cotizaciones: Cotizacion[];
  clientes: Cliente[];
  contactos: ContactoCliente[];
  onSelectCotizacion: (cot: Cotizacion) => void;
  onStateTransition: (cotId: number, nextEstado: EstadoCotizacion) => void;
  onCreateCotizacion: (clienteId: number, contactoId?: number, observaciones?: string) => void;
}

export const CotizacionesView: React.FC<CotizacionesViewProps> = ({
  cotizaciones,
  clientes,
  contactos,
  onSelectCotizacion,
  onStateTransition,
  onCreateCotizacion,
}) => {
  const [viewMode, setViewMode] = useState<'kanban' | 'list'>('kanban');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedClienteId, setSelectedClienteId] = useState<number>(clientes[0]?.id || 1);
  const [selectedContactoId, setSelectedContactoId] = useState<number | undefined>(undefined);
  const [observaciones, setObservaciones] = useState<string>('');

  const getClienteName = (id: number) => clientes.find((c) => c.id === id)?.empresa || 'Cliente';

  const clientContactos = contactos.filter((ct) => ct.clienteId === selectedClienteId);

  const handleCreateSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onCreateCotizacion(selectedClienteId, selectedContactoId, observaciones);
    setShowCreateModal(false);
    setObservaciones('');
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-600" />
            Pipeline Comercial & Cotizaciones
          </h2>
          <p className="text-xs text-slate-500">
            Flujo de trabajo de 14 estados desde Borrador hasta Facturación y Cierre de Expediente.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* Dual View Toggle */}
          <div className="bg-slate-100 p-1 rounded-lg flex items-center gap-1 border border-slate-200">
            <button
              onClick={() => setViewMode('kanban')}
              className={`px-3 py-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-all ${
                viewMode === 'kanban' ? 'bg-white text-blue-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <LayoutGrid className="w-3.5 h-3.5" /> Tablero Kanban
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-3 py-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-all ${
                viewMode === 'list' ? 'bg-white text-blue-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <List className="w-3.5 h-3.5" /> Vista Tabla
            </button>
          </div>

          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-xs"
          >
            <Plus className="w-4 h-4" /> Nueva Cotización
          </button>
        </div>
      </div>

      {/* Main View Area */}
      {viewMode === 'kanban' ? (
        <KanbanBoard
          cotizaciones={cotizaciones}
          clientes={clientes}
          onSelectCotizacion={onSelectCotizacion}
          onStateTransition={onStateTransition}
        />
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-slate-100 text-slate-600 font-semibold border-b border-slate-200">
                  <th className="p-3 pl-4">Número</th>
                  <th className="p-3">Cliente</th>
                  <th className="p-3">Estado del Pipeline</th>
                  <th className="p-3">Fecha Creación</th>
                  <th className="p-3 text-center">Eventos</th>
                  <th className="p-3 text-right">Valor Total (COP)</th>
                  <th className="p-3 text-center">Acción</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {cotizaciones.map((cot) => (
                  <tr key={cot.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-3 pl-4 font-bold text-blue-700 font-mono">{cot.numeroCotizacion}</td>
                    <td className="p-3 font-semibold text-slate-900">{getClienteName(cot.clienteId)}</td>
                    <td className="p-3">
                      <StateBadge estado={cot.estado} size="sm" />
                    </td>
                    <td className="p-3 font-mono text-[11px] text-slate-500">
                      {new Date(cot.fechaCreacion).toLocaleDateString('es-CO')}
                    </td>
                    <td className="p-3 text-center font-bold text-slate-700">{cot.eventos.length}</td>
                    <td className="p-3 text-right font-black text-slate-900">
                      ${cot.valorTotal.toLocaleString('es-CO')}
                    </td>
                    <td className="p-3 text-center">
                      <button
                        onClick={() => onSelectCotizacion(cot)}
                        className="bg-blue-50 text-blue-700 hover:bg-blue-100 font-semibold px-2.5 py-1 rounded-md text-xs inline-flex items-center gap-1"
                      >
                        <Eye className="w-3 h-3" /> Ver Detalle
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Modal Nueva Cotización */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-md p-6">
            <h3 className="text-base font-bold text-slate-900 mb-4">Iniciar Nueva Cotización (Borrador)</h3>
            <form onSubmit={handleCreateSubmit} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Seleccionar Cliente</label>
                <select
                  value={selectedClienteId}
                  onChange={(e) => {
                    const cid = Number(e.target.value);
                    setSelectedClienteId(cid);
                    setSelectedContactoId(undefined);
                  }}
                  className="w-full p-2 border border-slate-200 rounded-lg font-medium"
                >
                  {clientes.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.empresa} ({c.tipoCliente})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Contacto Atención (Opcional)</label>
                <select
                  value={selectedContactoId || ''}
                  onChange={(e) => setSelectedContactoId(e.target.value ? Number(e.target.value) : undefined)}
                  className="w-full p-2 border border-slate-200 rounded-lg"
                >
                  <option value="">Seleccionar contacto del cliente...</option>
                  {clientContactos.map((ct) => (
                    <option key={ct.id} value={ct.id}>
                      {ct.nombre} — {ct.cargo}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Observaciones / Propósito</label>
                <textarea
                  rows={3}
                  value={observaciones}
                  onChange={(e) => setObservaciones(e.target.value)}
                  placeholder="Ej: Servicio de ambulancia TAB + médico para cobertura de torneo institucional..."
                  className="w-full p-2 border border-slate-200 rounded-lg"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-3 py-2 bg-slate-100 text-slate-700 font-semibold rounded-lg"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg"
                >
                  Crear Borrador
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
