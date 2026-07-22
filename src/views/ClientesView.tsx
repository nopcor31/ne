import React, { useState } from 'react';
import {
  Cliente,
  ContactoCliente,
  InteraccionCRM,
  Tarea,
  Ciudad,
  TipoCliente,
  TipoInteraccionCRM,
  PrioridadTarea,
} from '../types';
import {
  Users,
  Plus,
  Building,
  Phone,
  Mail,
  MapPin,
  Calendar,
  MessageSquare,
  CheckCircle,
  X,
  UserPlus,
  Clock,
  Briefcase,
} from 'lucide-react';

interface ClientesViewProps {
  clientes: Cliente[];
  contactos: ContactoCliente[];
  interacciones: InteraccionCRM[];
  tareas: Tarea[];
  ciudades: Ciudad[];
  onAddCliente: (nuevo: Partial<Cliente>) => void;
  onAddContacto: (nuevo: Partial<ContactoCliente>) => void;
  onAddInteraccion: (nuevo: Partial<InteraccionCRM>) => void;
  onAddTarea: (nuevo: Partial<Tarea>) => void;
}

export const ClientesView: React.FC<ClientesViewProps> = ({
  clientes,
  contactos,
  interacciones,
  tareas,
  ciudades,
  onAddCliente,
  onAddContacto,
  onAddInteraccion,
  onAddTarea,
}) => {
  const [selectedCliente, setSelectedCliente] = useState<Cliente | null>(null);
  const [filterTipo, setFilterTipo] = useState<string>('TODOS');
  const [showClienteModal, setShowClienteModal] = useState(false);
  const [showInteraccionModal, setShowInteraccionModal] = useState(false);
  const [showTareaModal, setShowTareaModal] = useState(false);

  // New forms states
  const [newCliente, setNewCliente] = useState<Partial<Cliente>>({
    empresa: '',
    nit: '',
    correoPrincipal: '',
    telefonoPrincipal: '',
    tipoCliente: TipoCliente.NORMAL,
    sector: '',
    ciudadId: 1,
    direccion: '',
  });

  const [newInteraccion, setNewInteraccion] = useState<Partial<InteraccionCRM>>({
    tipo: TipoInteraccionCRM.LLAMADA,
    asunto: '',
    descripcion: '',
  });

  const [newTarea, setNewTarea] = useState<Partial<Tarea>>({
    titulo: '',
    descripcion: '',
    prioridad: PrioridadTarea.MEDIA,
    fechaVencimiento: new Date().toISOString().split('T')[0],
  });

  const getCiudadNombre = (id: number) => ciudades.find((c) => c.id === id)?.nombre || 'Ciudad';

  const filteredClientes = clientes.filter((c) => {
    if (filterTipo !== 'TODOS' && c.tipoCliente !== filterTipo) return false;
    return true;
  });

  const handleSaveCliente = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCliente.empresa || !newCliente.nit) return;
    onAddCliente(newCliente);
    setShowClienteModal(false);
    setNewCliente({
      empresa: '',
      nit: '',
      correoPrincipal: '',
      telefonoPrincipal: '',
      tipoCliente: TipoCliente.NORMAL,
      sector: '',
      ciudadId: 1,
      direccion: '',
    });
  };

  const handleSaveInteraccion = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCliente || !newInteraccion.asunto) return;
    onAddInteraccion({
      ...newInteraccion,
      clienteId: selectedCliente.id,
      fechaHora: new Date().toISOString(),
      usuarioId: 1,
    });
    setShowInteraccionModal(false);
    setNewInteraccion({ tipo: TipoInteraccionCRM.LLAMADA, asunto: '', descripcion: '' });
  };

  const handleSaveTarea = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCliente || !newTarea.titulo) return;
    onAddTarea({
      ...newTarea,
      clienteId: selectedCliente.id,
      completada: false,
      usuarioAsignadoId: 1,
      usuarioCreadorId: 1,
    });
    setShowTareaModal(false);
    setNewTarea({
      titulo: '',
      descripcion: '',
      prioridad: PrioridadTarea.MEDIA,
      fechaVencimiento: new Date().toISOString().split('T')[0],
    });
  };

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Users className="w-5 h-5 text-blue-600" />
            Gestión de Clientes & CRM Operativo
          </h2>
          <p className="text-xs text-slate-500">
            Ficha técnica de clientes, contactos, historial de interacciones y tareas comerciales.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={filterTipo}
            onChange={(e) => setFilterTipo(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-lg text-xs px-3 py-2 font-medium"
          >
            <option value="TODOS">Todos los Clientes</option>
            <option value={TipoCliente.NORMAL}>Tarifa Normal</option>
            <option value={TipoCliente.ESPECIAL}>Cliente Especial (Tarifa Propia)</option>
          </select>

          <button
            onClick={() => setShowClienteModal(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs px-3.5 py-2 rounded-lg flex items-center gap-1.5 shadow-xs"
          >
            <Plus className="w-4 h-4" /> Nuevo Cliente
          </button>
        </div>
      </div>

      {/* Main Content: Table + Detail Drawer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Clients Table */}
        <div className={`bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden ${selectedCliente ? 'lg:col-span-7' : 'lg:col-span-12'}`}>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
                  <th className="p-3 pl-4">Empresa / Razón Social</th>
                  <th className="p-3">NIT</th>
                  <th className="p-3">Tipo</th>
                  <th className="p-3">Ciudad</th>
                  <th className="p-3">Contacto Directo</th>
                  <th className="p-3 text-center">Acción</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {filteredClientes.map((c) => {
                  const isSelected = selectedCliente?.id === c.id;
                  const cContactos = contactos.filter((ct) => ct.clienteId === c.id);
                  const principalContact = cContactos.find((ct) => ct.esPrincipal) || cContactos[0];

                  return (
                    <tr
                      key={c.id}
                      onClick={() => setSelectedCliente(c)}
                      className={`cursor-pointer transition-colors ${
                        isSelected ? 'bg-blue-50/80 font-medium' : 'hover:bg-slate-50'
                      }`}
                    >
                      <td className="p-3 pl-4">
                        <p className="font-bold text-slate-900">{c.empresa}</p>
                        <p className="text-[10px] text-slate-400">{c.sector || 'Salud / Médico'}</p>
                      </td>
                      <td className="p-3 font-mono text-slate-600">{c.nit}</td>
                      <td className="p-3">
                        {c.tipoCliente === TipoCliente.ESPECIAL ? (
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
                            ESPECIAL
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-100 text-slate-600">
                            NORMAL
                          </span>
                        )}
                      </td>
                      <td className="p-3">{getCiudadNombre(c.ciudadId)}</td>
                      <td className="p-3">
                        <p className="font-semibold text-slate-800">{principalContact?.nombre || 'Sin contacto'}</p>
                        <p className="text-[10px] text-slate-400">{principalContact?.correo}</p>
                      </td>
                      <td className="p-3 text-center">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedCliente(c);
                          }}
                          className="text-xs font-semibold text-blue-600 hover:underline"
                        >
                          Ver Ficha CRM
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Client Detail Drawer */}
        {selectedCliente && (
          <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200 shadow-lg p-5 space-y-5 animate-in fade-in duration-150">
            <div className="flex items-start justify-between border-b border-slate-200 pb-3">
              <div>
                <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-blue-100 text-blue-800">
                  Ficha Técnica Cliente #{selectedCliente.id}
                </span>
                <h3 className="text-base font-bold text-slate-900 mt-1">{selectedCliente.empresa}</h3>
                <p className="text-xs text-slate-500 font-mono">NIT: {selectedCliente.nit}</p>
              </div>
              <button
                onClick={() => setSelectedCliente(null)}
                className="p-1 text-slate-400 hover:text-slate-800 rounded-lg hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Basic Info */}
            <div className="space-y-2 text-xs text-slate-700 bg-slate-50 p-3.5 rounded-lg border border-slate-200">
              <p className="flex items-center gap-2">
                <Mail className="w-3.5 h-3.5 text-slate-400" />
                <span className="font-semibold">{selectedCliente.correoPrincipal}</span>
              </p>
              <p className="flex items-center gap-2">
                <Phone className="w-3.5 h-3.5 text-slate-400" />
                <span>{selectedCliente.telefonoPrincipal}</span>
              </p>
              <p className="flex items-center gap-2">
                <MapPin className="w-3.5 h-3.5 text-slate-400" />
                <span>{selectedCliente.direccion || 'Sin dirección registrada'}</span>
              </p>
            </div>

            {/* Contacts Section */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Contactos Registrados
                </h4>
              </div>
              <div className="space-y-2">
                {contactos
                  .filter((ct) => ct.clienteId === selectedCliente.id)
                  .map((ct) => (
                    <div key={ct.id} className="p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                      <p className="font-bold text-slate-900 flex items-center justify-between">
                        <span>{ct.nombre}</span>
                        {ct.esPrincipal && (
                          <span className="text-[9px] bg-blue-100 text-blue-700 font-bold px-1.5 py-0.5 rounded">
                            PRINCIPAL
                          </span>
                        )}
                      </p>
                      <p className="text-[11px] text-slate-500">{ct.cargo}</p>
                      <p className="text-[11px] text-slate-600 mt-1">{ct.correo} · {ct.telefono}</p>
                    </div>
                  ))}
              </div>
            </div>

            {/* Interacciones CRM */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Interacciones CRM
                </h4>
                <button
                  onClick={() => setShowInteraccionModal(true)}
                  className="text-[11px] font-bold text-blue-600 hover:underline flex items-center gap-1"
                >
                  <Plus className="w-3 h-3" /> Registrar
                </button>
              </div>

              <div className="space-y-2 max-h-40 overflow-y-auto pr-1">
                {interacciones
                  .filter((it) => it.clienteId === selectedCliente.id)
                  .map((it) => (
                    <div key={it.id} className="p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-slate-900">{it.asunto}</span>
                        <span className="text-[9px] font-semibold px-1.5 py-0.5 rounded bg-slate-200 text-slate-700">
                          {it.tipo}
                        </span>
                      </div>
                      <p className="text-slate-600 mt-1 leading-relaxed">{it.descripcion}</p>
                    </div>
                  ))}
              </div>
            </div>

            {/* Tareas Pendientes */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                  Tareas Pendientes
                </h4>
                <button
                  onClick={() => setShowTareaModal(true)}
                  className="text-[11px] font-bold text-blue-600 hover:underline flex items-center gap-1"
                >
                  <Plus className="w-3 h-3" /> Crear Tarea
                </button>
              </div>

              <div className="space-y-2">
                {tareas
                  .filter((t) => t.clienteId === selectedCliente.id)
                  .map((t) => (
                    <div key={t.id} className="p-2.5 bg-amber-50/60 rounded-lg border border-amber-200 text-xs">
                      <div className="flex items-center justify-between font-bold text-amber-900">
                        <span>{t.titulo}</span>
                        <span className="text-[9px] bg-amber-200 text-amber-800 px-1.5 py-0.5 rounded">
                          Vence: {t.fechaVencimiento}
                        </span>
                      </div>
                      {t.descripcion && <p className="text-amber-800/80 mt-1">{t.descripcion}</p>}
                    </div>
                  ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Modal Nuevo Cliente */}
      {showClienteModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-md p-6 animate-in fade-in duration-200">
            <h3 className="text-base font-bold text-slate-900 mb-4">Registrar Nuevo Cliente</h3>
            <form onSubmit={handleSaveCliente} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Empresa / Razón Social</label>
                <input
                  type="text"
                  required
                  value={newCliente.empresa}
                  onChange={(e) => setNewCliente({ ...newCliente, empresa: e.target.value })}
                  className="w-full p-2 border border-slate-200 rounded-lg"
                  placeholder="Ej: Hospital Universitario S.A."
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">NIT</label>
                  <input
                    type="text"
                    required
                    value={newCliente.nit}
                    onChange={(e) => setNewCliente({ ...newCliente, nit: e.target.value })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                    placeholder="900.123.456-1"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Tipo de Tarifa</label>
                  <select
                    value={newCliente.tipoCliente}
                    onChange={(e) => setNewCliente({ ...newCliente, tipoCliente: e.target.value as TipoCliente })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  >
                    <option value={TipoCliente.NORMAL}>NORMAL (General)</option>
                    <option value={TipoCliente.ESPECIAL}>ESPECIAL (Propia)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Correo Principal</label>
                <input
                  type="email"
                  value={newCliente.correoPrincipal}
                  onChange={(e) => setNewCliente({ ...newCliente, correoPrincipal: e.target.value })}
                  className="w-full p-2 border border-slate-200 rounded-lg"
                  placeholder="compras@empresa.com"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Teléfono Principal</label>
                <input
                  type="text"
                  value={newCliente.telefonoPrincipal}
                  onChange={(e) => setNewCliente({ ...newCliente, telefonoPrincipal: e.target.value })}
                  className="w-full p-2 border border-slate-200 rounded-lg"
                  placeholder="601-234-5678"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setShowClienteModal(false)}
                  className="px-3 py-2 bg-slate-100 text-slate-700 font-semibold rounded-lg"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg"
                >
                  Guardar Cliente
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Nueva Interaccion */}
      {showInteraccionModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-md p-6">
            <h3 className="text-base font-bold text-slate-900 mb-4">Registrar Interacción CRM</h3>
            <form onSubmit={handleSaveInteraccion} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Tipo de Interacción</label>
                <select
                  value={newInteraccion.tipo}
                  onChange={(e) =>
                    setNewInteraccion({ ...newInteraccion, tipo: e.target.value as TipoInteraccionCRM })
                  }
                  className="w-full p-2 border border-slate-200 rounded-lg"
                >
                  <option value={TipoInteraccionCRM.LLAMADA}>Llamada Telefónica</option>
                  <option value={TipoInteraccionCRM.REUNION}>Reunión / Presentación</option>
                  <option value={TipoInteraccionCRM.EMAIL}>Correo Electrónico</option>
                  <option value={TipoInteraccionCRM.VISITA}>Visita Institucional</option>
                  <option value={TipoInteraccionCRM.NOTA}>Nota Interna</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Asunto</label>
                <input
                  type="text"
                  required
                  value={newInteraccion.asunto}
                  onChange={(e) => setNewInteraccion({ ...newInteraccion, asunto: e.target.value })}
                  className="w-full p-2 border border-slate-200 rounded-lg"
                  placeholder="Ej: Seguimiento a solicitud de cotización"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Detalles de la Conversación</label>
                <textarea
                  rows={3}
                  value={newInteraccion.descripcion}
                  onChange={(e) => setNewInteraccion({ ...newInteraccion, descripcion: e.target.value })}
                  className="w-full p-2 border border-slate-200 rounded-lg"
                  placeholder="Acuerdos, requerimientos o respuesta dada por el cliente..."
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setShowInteraccionModal(false)}
                  className="px-3 py-2 bg-slate-100 text-slate-700 font-semibold rounded-lg"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg"
                >
                  Guardar Registro
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal Nueva Tarea */}
      {showTareaModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl border border-slate-200 shadow-2xl w-full max-w-md p-6">
            <h3 className="text-base font-bold text-slate-900 mb-4">Crear Tarea Comercial</h3>
            <form onSubmit={handleSaveTarea} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Título de la Tarea</label>
                <input
                  type="text"
                  required
                  value={newTarea.titulo}
                  onChange={(e) => setNewTarea({ ...newTarea, titulo: e.target.value })}
                  className="w-full p-2 border border-slate-200 rounded-lg"
                  placeholder="Ej: Solicitar Orden de Compra corregida"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Prioridad</label>
                  <select
                    value={newTarea.prioridad}
                    onChange={(e) =>
                      setNewTarea({ ...newTarea, prioridad: e.target.value as PrioridadTarea })
                    }
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  >
                    <option value={PrioridadTarea.BAJA}>Baja</option>
                    <option value={PrioridadTarea.MEDIA}>Media</option>
                    <option value={PrioridadTarea.ALTA}>Alta</option>
                    <option value={PrioridadTarea.CRITICA}>Crítica</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Fecha Vencimiento</label>
                  <input
                    type="date"
                    required
                    value={newTarea.fechaVencimiento}
                    onChange={(e) => setNewTarea({ ...newTarea, fechaVencimiento: e.target.value })}
                    className="w-full p-2 border border-slate-200 rounded-lg"
                  />
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Descripción / Notas</label>
                <textarea
                  rows={2}
                  value={newTarea.descripcion}
                  onChange={(e) => setNewTarea({ ...newTarea, descripcion: e.target.value })}
                  className="w-full p-2 border border-slate-200 rounded-lg"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setShowTareaModal(false)}
                  className="px-3 py-2 bg-slate-100 text-slate-700 font-semibold rounded-lg"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg"
                >
                  Crear Tarea
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
