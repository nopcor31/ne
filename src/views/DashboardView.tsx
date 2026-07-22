import React from 'react';
import { Cotizacion, Cliente, Alerta, HistorialActividad, EstadoCotizacion } from '../types';
import { KpiCard } from '../components/KpiCard';
import { StateBadge } from '../components/StateBadge';
import {
  FileText,
  Clock,
  Building2,
  Calendar,
  Receipt,
  DollarSign,
  AlertTriangle,
  Activity,
  ArrowUpRight,
  ShieldAlert,
} from 'lucide-react';

interface DashboardViewProps {
  cotizaciones: Cotizacion[];
  clientes: Cliente[];
  alertas: Alerta[];
  historial: HistorialActividad[];
  onNavigateTab: (tab: any) => void;
  onSelectCotizacion: (cot: Cotizacion) => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  cotizaciones,
  clientes,
  alertas,
  historial,
  onNavigateTab,
  onSelectCotizacion,
}) => {
  // Metrics calculation
  const totalCotizadas = cotizaciones.length;
  const abiertas = cotizaciones.filter(
    (c) =>
      c.estado !== EstadoCotizacion.CERRADA &&
      c.estado !== EstadoCotizacion.RECHAZADA_CLIENTE &&
      c.estado !== EstadoCotizacion.PAGADA
  ).length;

  const pendCliente = cotizaciones.filter((c) => c.estado === EstadoCotizacion.ENVIADA_CLIENTE).length;
  const pendAreaMedica = cotizaciones.filter((c) => c.estado === EstadoCotizacion.PENDIENTE_AREA_MEDICA).length;
  const programadas = cotizaciones.filter((c) => c.estado === EstadoCotizacion.PROGRAMADA).length;
  const pendFacturacion = cotizaciones.filter(
    (c) => c.estado === EstadoCotizacion.PENDIENTE_FACTURACION || c.estado === EstadoCotizacion.OC_RECIBIDA
  ).length;

  const totalValorCotizado = cotizaciones.reduce((sum, c) => sum + c.valorTotal, 0);
  const totalValorFacturado = cotizaciones
    .filter((c) => c.estado === EstadoCotizacion.FACTURADA || c.estado === EstadoCotizacion.PAGADA)
    .reduce((sum, c) => sum + c.valorTotal, 0);

  const activeAlerts = alertas.filter((a) => a.activa);

  const getClienteName = (id: number) => clientes.find((c) => c.id === id)?.empresa || 'Cliente';

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-blue-900 text-white rounded-2xl p-6 shadow-md flex items-center justify-between">
        <div>
          <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-blue-500/30 text-blue-300 border border-blue-400/30 tracking-wider">
            Consola Principal
          </span>
          <h2 className="text-2xl font-black text-white mt-1">CRM Operativo Servicios Médicos NE</h2>
          <p className="text-xs text-slate-300 mt-1">
            Monitoreo en tiempo real de cotizaciones, aprobaciones médicas, programación y facturación.
          </p>
        </div>

        <button
          onClick={() => onNavigateTab('cotizaciones')}
          className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-2.5 rounded-xl shadow-sm transition-all flex items-center gap-2 shrink-0"
        >
          Gestor de Cotizaciones <ArrowUpRight className="w-4 h-4" />
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        <KpiCard
          title="Cotizaciones Abiertas"
          value={abiertas}
          subtext={`De un total de ${totalCotizadas} creadas`}
          icon={FileText}
          badge="En proceso"
          badgeType="info"
          colorClass="bg-blue-50 text-blue-600"
          onClick={() => onNavigateTab('cotizaciones')}
        />

        <KpiCard
          title="Pend. Cliente"
          value={pendCliente}
          subtext="Enviadas esperando respuesta"
          icon={Clock}
          badge="Seguimiento"
          badgeType="warning"
          colorClass="bg-purple-50 text-purple-600"
          onClick={() => onNavigateTab('cotizaciones')}
        />

        <KpiCard
          title="Pend. Área Médica"
          value={pendAreaMedica}
          subtext="En revisión técnica médica"
          icon={Building2}
          badge="Aprobación"
          badgeType="warning"
          colorClass="bg-amber-50 text-amber-600"
          onClick={() => onNavigateTab('areas')}
        />

        <KpiCard
          title="Programadas"
          value={programadas}
          subtext="Servicios con recursos asignados"
          icon={Calendar}
          badge="Operativo"
          badgeType="success"
          colorClass="bg-cyan-50 text-cyan-600"
          onClick={() => onNavigateTab('programacion')}
        />

        <KpiCard
          title="Pend. Facturación"
          value={pendFacturacion}
          subtext="Listas para emisión de factura"
          icon={Receipt}
          badge="Financiero"
          badgeType="info"
          colorClass="bg-orange-50 text-orange-600"
          onClick={() => onNavigateTab('facturacion')}
        />
      </div>

      {/* Financial Summary Strip */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-blue-50 text-blue-700 rounded-xl">
              <DollarSign className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase">Total Cotizado en Pipeline</p>
              <h3 className="text-2xl font-black text-slate-900 mt-0.5">
                ${totalValorCotizado.toLocaleString('es-CO')} COP
              </h3>
            </div>
          </div>
          <span className="text-xs font-bold text-blue-700 bg-blue-50 px-2.5 py-1 rounded-lg">
            Valor acumulado
          </span>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-3 bg-emerald-50 text-emerald-700 rounded-xl">
              <Receipt className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-semibold text-slate-500 uppercase">Total Facturado & Cobrado</p>
              <h3 className="text-2xl font-black text-slate-900 mt-0.5">
                ${totalValorFacturado.toLocaleString('es-CO')} COP
              </h3>
            </div>
          </div>
          <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg">
            Facturas ejecutadas
          </span>
        </div>
      </div>

      {/* Two Column Layout: Alerts & Activity Timeline */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active Alerts Panel */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
          <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-rose-600" />
              <h3 className="text-sm font-bold text-slate-800">Alertas Operativas Activas</h3>
            </div>
            <button
              onClick={() => onNavigateTab('alertas')}
              className="text-xs text-blue-600 font-semibold hover:underline"
            >
              Ver todas ({activeAlerts.length})
            </button>
          </div>

          <div className="p-4 flex-1 space-y-3">
            {activeAlerts.length === 0 ? (
              <div className="py-8 text-center text-xs text-slate-400">
                ✅ No hay alertas críticas ni advertencias activas en el sistema.
              </div>
            ) : (
              activeAlerts.map((alerta) => (
                <div
                  key={alerta.id}
                  className={`p-3.5 rounded-lg border flex items-start gap-3 transition-all ${
                    alerta.prioridad === 'CRITICA'
                      ? 'bg-rose-50/60 border-rose-200 text-rose-900'
                      : 'bg-amber-50/60 border-amber-200 text-amber-900'
                  }`}
                >
                  <AlertTriangle
                    className={`w-4 h-4 mt-0.5 shrink-0 ${
                      alerta.prioridad === 'CRITICA' ? 'text-rose-600' : 'text-amber-600'
                    }`}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-xs font-bold">{alerta.titulo}</p>
                      <span className="text-[10px] opacity-75">
                        {new Date(alerta.fechaCreacion).toLocaleDateString('es-CO')}
                      </span>
                    </div>
                    <p className="text-xs mt-1 leading-relaxed">{alerta.mensaje}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Activity Timeline */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden flex flex-col">
          <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-blue-600" />
              <h3 className="text-sm font-bold text-slate-800">Actividad Reciente del Sistema</h3>
            </div>
            <button
              onClick={() => onNavigateTab('historial')}
              className="text-xs text-blue-600 font-semibold hover:underline"
            >
              Bitácora Completa
            </button>
          </div>

          <div className="p-4 flex-1 space-y-3">
            {historial.slice(0, 5).map((item) => (
              <div key={item.id} className="flex items-start gap-3 text-xs">
                <div className="w-2 h-2 rounded-full bg-blue-600 mt-1.5 shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-slate-900 truncate">{item.accion}</span>
                    <span className="text-[10px] text-slate-400">
                      {new Date(item.fechaHora).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  {item.detalle && <p className="text-slate-500 mt-0.5 line-clamp-1">{item.detalle}</p>}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quotations Quick Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-800">Últimas Cotizaciones Registradas</h3>
          <button
            onClick={() => onNavigateTab('cotizaciones')}
            className="text-xs text-blue-600 font-semibold hover:underline"
          >
            Ver Pipeline Kanban
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-100 text-slate-600 font-semibold border-b border-slate-200">
                <th className="p-3 pl-4">Número</th>
                <th className="p-3">Cliente</th>
                <th className="p-3">Estado</th>
                <th className="p-3 text-right">Valor Total</th>
                <th className="p-3 text-center">Acción</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {cotizaciones.slice(0, 5).map((cot) => (
                <tr key={cot.id} className="hover:bg-slate-50 transition-colors">
                  <td className="p-3 pl-4 font-bold text-blue-700">{cot.numeroCotizacion}</td>
                  <td className="p-3 font-medium text-slate-900">{getClienteName(cot.clienteId)}</td>
                  <td className="p-3">
                    <StateBadge estado={cot.estado} size="sm" />
                  </td>
                  <td className="p-3 text-right font-bold text-slate-900">
                    ${cot.valorTotal.toLocaleString('es-CO')}
                  </td>
                  <td className="p-3 text-center">
                    <button
                      onClick={() => onSelectCotizacion(cot)}
                      className="text-xs font-semibold text-blue-600 hover:text-blue-800"
                    >
                      Abrir
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
