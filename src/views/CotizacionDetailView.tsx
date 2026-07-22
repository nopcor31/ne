import React, { useState } from 'react';
import {
  Cotizacion,
  Cliente,
  ContactoCliente,
  Servicio,
  Ciudad,
  Festivo,
  Tarifa,
  Evento,
  ExtraEvento,
  EstadoCotizacion,
  TipoExtra,
  ConfiguracionSistema,
} from '../types';
import { StateBadge } from '../components/StateBadge';
import { ProgressSteps } from '../components/ProgressSteps';
import { obtenerProximosEstados, ESTADO_LABELS } from '../services/stateMachine';
import { calcularEvento } from '../services/calculationEngine';
import { PdfViewerModal } from '../components/PdfViewerModal';
import {
  ArrowLeft,
  FileText,
  Plus,
  Trash2,
  Copy,
  Mail,
  Calendar,
  Clock,
  MapPin,
  CheckCircle,
  DollarSign,
  Send,
  Building2,
  PackageCheck,
  Receipt,
  Printer,
} from 'lucide-react';

interface CotizacionDetailViewProps {
  cotizacion: Cotizacion;
  cliente: Cliente | undefined;
  contacto: ContactoCliente | undefined;
  servicios: Servicio[];
  ciudades: Ciudad[];
  festivos: Festivo[];
  tarifas: Tarifa[];
  config: ConfiguracionSistema;
  onBack: () => void;
  onStateTransition: (cotId: number, nextEstado: EstadoCotizacion) => void;
  onAddEvento: (cotId: number, evento: Partial<Evento>) => void;
  onDeleteEvento: (cotId: number, eventoId: number) => void;
  onDuplicateEvento: (cotId: number, eventoId: number) => void;
}

export const CotizacionDetailView: React.FC<CotizacionDetailViewProps> = ({
  cotizacion,
  cliente,
  contacto,
  servicios,
  ciudades,
  festivos,
  tarifas,
  config,
  onBack,
  onStateTransition,
  onAddEvento,
  onDeleteEvento,
  onDuplicateEvento,
}) => {
  const [showEventModal, setShowEventModal] = useState(false);
  const [showPdfModal, setShowPdfModal] = useState(false);

  // New event form state
  const [newEvent, setNewEvent] = useState<Partial<Evento>>({
    servicioId: 1,
    fecha: new Date().toISOString().split('T')[0],
    horaInicio: '08:00',
    horaFin: '17:00',
    ciudadId: 1,
    direccion: cliente?.direccion || 'Sede Principal',
    contacto: contacto?.nombre || 'Contacto Directo',
    telefono: contacto?.telefono || '300-000-0000',
    observaciones: '',
    extras: [],
  });

  const [extraInput, setExtraInput] = useState<{ tipo: TipoExtra; descripcion: string; valor: number }>({
    tipo: TipoExtra.PEAJE,
    descripcion: '',
    valor: 50000,
  });

  // Calculate live preview for new event modal
  const livePreview = calcularEvento(newEvent, cliente || null, festivos, tarifas);

  const getServicioNombre = (id: number) => servicios.find((s) => s.id === id)?.nombre || 'Servicio';
  const getCiudadNombre = (id: number) => ciudades.find((c) => c.id === id)?.nombre || 'Ciudad';

  const nextStates = obtenerProximosEstados(cotizacion.estado);

  const handleAddExtraToForm = () => {
    if (!extraInput.descripcion || extraInput.valor <= 0) return;
    const extrasList = newEvent.extras || [];
    setNewEvent({
      ...newEvent,
      extras: [...extrasList, { id: Date.now(), ...extraInput }],
    });
    setExtraInput({ tipo: TipoExtra.PEAJE, descripcion: '', valor: 50000 });
  };

  const handleRemoveExtraFromForm = (id: number) => {
    setNewEvent({
      ...newEvent,
      extras: (newEvent.extras || []).filter((e) => e.id !== id),
    });
  };

  const handleSaveEventoSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onAddEvento(cotizacion.id, newEvent);
    setShowEventModal(false);
  };

  return (
    <div className="space-y-6">
      {/* Top Header & Navigation */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="p-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl transition-colors"
            title="Volver a la lista"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>

          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-black text-blue-700 font-mono">{cotizacion.numeroCotizacion}</span>
              <StateBadge estado={cotizacion.estado} size="md" />
            </div>
            <p className="text-xs text-slate-600 mt-0.5 font-medium">
              Cliente: <span className="text-slate-900 font-bold">{cliente?.empresa}</span> · Atn: {contacto?.nombre || 'Contacto Principal'}
            </p>
          </div>
        </div>

        {/* Total Price & Primary Actions */}
        <div className="flex items-center gap-4">
          <div className="text-right border-r border-slate-200 pr-4">
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Valor Total Oferta</p>
            <p className="text-2xl font-black text-slate-900">${cotizacion.valorTotal.toLocaleString('es-CO')} COP</p>
          </div>

          <button
            onClick={() => setShowPdfModal(true)}
            className="bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs px-3.5 py-2.5 rounded-xl shadow-xs flex items-center gap-1.5 transition-colors"
          >
            <Printer className="w-4 h-4" /> Generar PDF
          </button>
        </div>
      </div>

      {/* Pipeline Stepper */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-xs">
        <ProgressSteps currentEstado={cotizacion.estado} />
      </div>

      {/* Contextual Action Bar for State Transitions */}
      {nextStates.length > 0 && (
        <div className="bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 p-4 rounded-2xl border border-blue-200/80 flex flex-col sm:flex-row items-center justify-between gap-3 shadow-2xs">
          <div className="flex items-center gap-2">
            <Send className="w-4 h-4 text-blue-700" />
            <p className="text-xs font-bold text-slate-800">
              Acciones disponibles para el estado actual ({ESTADO_LABELS[cotizacion.estado]}):
            </p>
          </div>

          <div className="flex items-center gap-2">
            {nextStates.map((ns) => (
              <button
                key={ns}
                onClick={() => onStateTransition(cotizacion.id, ns)}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-4 py-2 rounded-xl shadow-xs transition-colors flex items-center gap-1.5"
              >
                Avanzar a: {ESTADO_LABELS[ns]}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Events Breakdown Section */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3">
          <div>
            <h3 className="text-base font-bold text-slate-900">Eventos de Servicio Programados</h3>
            <p className="text-xs text-slate-500">
              Cálculo de horas diurnas/nocturnas, tipo de día (festivo/ordinario) y recargos aplicados.
            </p>
          </div>

          <button
            onClick={() => setShowEventModal(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs px-3.5 py-2 rounded-xl flex items-center gap-1.5 shadow-xs"
          >
            <Plus className="w-4 h-4" /> Agregar Evento
          </button>
        </div>

        {/* Events Table */}
        <div className="space-y-4">
          {cotizacion.eventos.length === 0 ? (
            <div className="p-8 text-center border-2 border-dashed border-slate-200 rounded-xl text-xs text-slate-400">
              No se han agregado eventos a esta cotización. Haga clic en "Agregar Evento" para configurar la cobertura.
            </div>
          ) : (
            cotizacion.eventos.map((ev, index) => (
              <div
                key={ev.id}
                className="bg-slate-50 rounded-xl border border-slate-200 p-4 space-y-3 hover:border-blue-300 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-800 font-bold text-xs flex items-center justify-center">
                      {index + 1}
                    </span>
                    <div>
                      <h4 className="text-sm font-bold text-slate-900">{getServicioNombre(ev.servicioId)}</h4>
                      <p className="text-xs text-slate-500 flex items-center gap-2 mt-0.5">
                        <Calendar className="w-3.5 h-3.5 text-slate-400" /> {ev.fecha} ({ev.tipoDia}) ·
                        <Clock className="w-3.5 h-3.5 text-slate-400" /> {ev.horaInicio} a {ev.horaFin} ·
                        <MapPin className="w-3.5 h-3.5 text-slate-400" /> {getCiudadNombre(ev.ciudadId)}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => onDuplicateEvento(cotizacion.id, ev.id)}
                      className="p-1.5 text-slate-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      title="Duplicar este evento"
                    >
                      <Copy className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onDeleteEvento(cotizacion.id, ev.id)}
                      className="p-1.5 text-slate-500 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                      title="Eliminar evento"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Calculation Details Box */}
                <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 bg-white p-3 rounded-lg border border-slate-200 text-xs">
                  <div>
                    <span className="text-slate-400 font-medium">Horas Diurnas:</span>
                    <p className="font-bold text-slate-800">{ev.horasDiurnas} h</p>
                    <p className="text-[10px] text-slate-400">${ev.valorHorasDiurnas.toLocaleString('es-CO')}</p>
                  </div>
                  <div>
                    <span className="text-slate-400 font-medium">Horas Nocturnas:</span>
                    <p className="font-bold text-slate-800">{ev.horasNocturnas} h</p>
                    <p className="text-[10px] text-slate-400">${ev.valorHorasNocturnas.toLocaleString('es-CO')}</p>
                  </div>
                  <div>
                    <span className="text-slate-400 font-medium">Extras & Peajes:</span>
                    <p className="font-bold text-slate-800">${ev.valorExtras.toLocaleString('es-CO')}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-slate-400 font-medium">Subtotal Evento:</span>
                    <p className="font-black text-sm text-blue-700">${ev.valorEvento.toLocaleString('es-CO')}</p>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Event Add Modal */}
      {showEventModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 overflow-y-auto">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-xl p-6 my-8">
            <h3 className="text-base font-bold text-slate-900 mb-4">Agregar Evento a la Cotización</h3>

            <form onSubmit={handleSaveEventoSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Servicio Asistencial</label>
                <select
                  value={newEvent.servicioId}
                  onChange={(e) => setNewEvent({ ...newEvent, servicioId: Number(e.target.value) })}
                  className="w-full p-2 border border-slate-200 rounded-lg font-medium"
                >
                  {servicios.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.nombre}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Fecha Evento</label>
                  <input
                    type="date"
                    required
                    value={newEvent.fecha}
                    onChange={(e) => setNewEvent({ ...newEvent, fecha: e.target.value })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Hora Inicio</label>
                  <input
                    type="time"
                    required
                    value={newEvent.horaInicio}
                    onChange={(e) => setNewEvent({ ...newEvent, horaInicio: e.target.value })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Hora Fin</label>
                  <input
                    type="time"
                    required
                    value={newEvent.horaFin}
                    onChange={(e) => setNewEvent({ ...newEvent, horaFin: e.target.value })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Ciudad de Cobertura</label>
                  <select
                    value={newEvent.ciudadId}
                    onChange={(e) => setNewEvent({ ...newEvent, ciudadId: Number(e.target.value) })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  >
                    {ciudades.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.nombre}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Dirección Evento</label>
                  <input
                    type="text"
                    value={newEvent.direccion}
                    onChange={(e) => setNewEvent({ ...newEvent, direccion: e.target.value })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  />
                </div>
              </div>

              {/* Automatic Live Calculation Box */}
              <div className="bg-blue-50/80 p-3.5 rounded-xl border border-blue-200 text-xs space-y-1">
                <p className="font-bold text-blue-900 uppercase text-[10px]">
                  CÁLCULO AUTOMÁTICO DE TARIFAS Y FRANSAS
                </p>
                <div className="grid grid-cols-2 gap-2 text-slate-700 pt-1">
                  <div>
                    <span>Tipo de Día: </span>
                    <strong className="text-blue-900">{livePreview.tipoDia}</strong>
                  </div>
                  <div>
                    <span>Horas Diurnas: </span>
                    <strong className="text-blue-900">{livePreview.horasDiurnas} h</strong> (${livePreview.valorHorasDiurnas.toLocaleString('es-CO')})
                  </div>
                  <div>
                    <span>Horas Nocturnas: </span>
                    <strong className="text-blue-900">{livePreview.horasNocturnas} h</strong> (${livePreview.valorHorasNocturnas.toLocaleString('es-CO')})
                  </div>
                  <div>
                    <span>Valor Evento: </span>
                    <strong className="text-emerald-700 font-black">${livePreview.valorEvento.toLocaleString('es-CO')}</strong>
                  </div>
                </div>
              </div>

              {/* Extras Adder */}
              <div className="border-t border-slate-200 pt-3">
                <label className="block font-semibold text-slate-700 mb-1">Agregar Peajes o Recargos</label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    placeholder="Descripción (ej: Peaje Autopista)"
                    value={extraInput.descripcion}
                    onChange={(e) => setExtraInput({ ...extraInput, descripcion: e.target.value })}
                    className="flex-1 p-1.5 border border-slate-200 rounded-lg text-xs"
                  />
                  <input
                    type="number"
                    step="5000"
                    placeholder="Valor"
                    value={extraInput.valor}
                    onChange={(e) => setExtraInput({ ...extraInput, valor: Number(e.target.value) })}
                    className="w-24 p-1.5 border border-slate-200 rounded-lg text-xs font-mono"
                  />
                  <button
                    type="button"
                    onClick={handleAddExtraToForm}
                    className="bg-slate-800 text-white text-xs px-3 py-1.5 rounded-lg font-semibold"
                  >
                    +
                  </button>
                </div>

                <div className="space-y-1">
                  {(newEvent.extras || []).map((ext) => (
                    <div key={ext.id} className="flex items-center justify-between bg-slate-100 p-1.5 rounded text-[11px]">
                      <span>{ext.descripcion}</span>
                      <div className="flex items-center gap-2">
                        <span className="font-bold">${ext.valor.toLocaleString('es-CO')}</span>
                        <button
                          type="button"
                          onClick={() => handleRemoveExtraFromForm(ext.id!)}
                          className="text-rose-600 font-bold"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setShowEventModal(false)}
                  className="px-3 py-2 bg-slate-100 text-slate-700 font-semibold rounded-lg"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg"
                >
                  Guardar Evento
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* PDF View Modal */}
      {showPdfModal && (
        <PdfViewerModal
          cotizacion={cotizacion}
          cliente={cliente}
          contacto={contacto}
          config={config}
          servicios={servicios}
          ciudades={ciudades}
          onClose={() => setShowPdfModal(false)}
          onSendEmail={() => {
            alert(`Correo de cotización ${cotizacion.numeroCotizacion} enviado exitosamente vía Outlook COM.`);
            onStateTransition(cotizacion.id, EstadoCotizacion.ENVIADA_CLIENTE);
            setShowPdfModal(false);
          }}
        />
      )}
    </div>
  );
};
