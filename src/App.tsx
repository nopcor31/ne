import React, { useState } from 'react';
import {
  Cliente,
  ContactoCliente,
  InteraccionCRM,
  Tarea,
  Cotizacion,
  Evento,
  Tarifa,
  Festivo,
  AreaMedica,
  Programacion,
  OrdenCompra,
  Factura,
  Alerta,
  HistorialActividad,
  ConfiguracionSistema,
  EstadoCotizacion,
  TipoAlerta,
} from './types';
import {
  INITIAL_USUARIOS,
  INITIAL_CIUDADES,
  INITIAL_SERVICIOS,
  INITIAL_CLIENTES,
  INITIAL_CONTACTOS,
  INITIAL_INTERACCIONES,
  INITIAL_TAREAS,
  INITIAL_FESTIVOS,
  INITIAL_TARIFAS,
  INITIAL_COTIZACIONES,
  INITIAL_AREAS_MEDICAS,
  INITIAL_PROGRAMACIONES,
  INITIAL_ORDENES_COMPRA,
  INITIAL_FACTURAS,
  INITIAL_ALERTAS,
  INITIAL_HISTORIAL,
  INITIAL_CONFIGURACION,
} from './data/mockData';
import { Sidebar, TabType } from './components/Sidebar';
import { Topbar } from './components/Topbar';
import { DashboardView } from './views/DashboardView';
import { ClientesView } from './views/ClientesView';
import { TarifasView } from './views/TarifasView';
import { CotizacionesView } from './views/CotizacionesView';
import { CotizacionDetailView } from './views/CotizacionDetailView';
import { ProgramacionView } from './views/ProgramacionView';
import { AreasMedicasView } from './views/AreasMedicasView';
import { OrdenesCompraView } from './views/OrdenesCompraView';
import { FacturacionView } from './views/FacturacionView';
import { AlertasView } from './views/AlertasView';
import { HistorialView } from './views/HistorialView';
import { ConfiguracionView } from './views/ConfiguracionView';
import { PythonAuditView } from './views/PythonAuditView';

import { esTransicionValida } from './services/stateMachine';
import { calcularEvento } from './services/calculationEngine';

export default function App() {
  const [activeTab, setActiveTab] = useState<TabType>('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCotizacion, setSelectedCotizacion] = useState<Cotizacion | null>(null);

  // Core Master States
  const [clientes, setClientes] = useState<Cliente[]>(INITIAL_CLIENTES);
  const [contactos, setContactos] = useState<ContactoCliente[]>(INITIAL_CONTACTOS);
  const [interacciones, setInteracciones] = useState<InteraccionCRM[]>(INITIAL_INTERACCIONES);
  const [tareas, setTareas] = useState<Tarea[]>(INITIAL_TAREAS);
  const [tarifas, setTarifas] = useState<Tarifa[]>(INITIAL_TARIFAS);
  const [festivos, setFestivos] = useState<Festivo[]>(INITIAL_FESTIVOS);
  const [cotizaciones, setCotizaciones] = useState<Cotizacion[]>(INITIAL_COTIZACIONES);
  const [areasMedicas, setAreasMedicas] = useState<AreaMedica[]>(INITIAL_AREAS_MEDICAS);
  const [programaciones, setProgramaciones] = useState<Programacion[]>(INITIAL_PROGRAMACIONES);
  const [ordenesCompra, setOrdenesCompra] = useState<OrdenCompra[]>(INITIAL_ORDENES_COMPRA);
  const [facturas, setFacturas] = useState<Factura[]>(INITIAL_FACTURAS);
  const [alertas, setAlertas] = useState<Alerta[]>(INITIAL_ALERTAS);
  const [historial, setHistorial] = useState<HistorialActividad[]>(INITIAL_HISTORIAL);
  const [config, setConfig] = useState<ConfiguracionSistema>(INITIAL_CONFIGURACION);

  // Transversal Audit Logger
  const registrarHistorial = (accion: string, entidadTipo: string, entidadId: number, detalle?: string) => {
    const nuevoRegistro: HistorialActividad = {
      id: Date.now(),
      fechaHora: new Date().toISOString(),
      usuarioId: 1,
      entidadTipo,
      entidadId,
      accion,
      detalle,
      esAutomatico: false,
    };
    setHistorial((prev) => [nuevoRegistro, ...prev]);
  };

  // State Transition Executor
  const handleStateTransition = (cotId: number, nextEstado: EstadoCotizacion) => {
    const targetCot = cotizaciones.find((c) => c.id === cotId);
    if (!targetCot) return;

    if (!esTransicionValida(targetCot.estado, nextEstado)) {
      alert(`Transición inválida de ${targetCot.estado} a ${nextEstado}`);
      return;
    }

    const updated = cotizaciones.map((c) => {
      if (c.id === cotId) {
        return {
          ...c,
          estado: nextEstado,
          fechaRespuestaCliente: nextEstado === EstadoCotizacion.ACEPTADA_CLIENTE ? new Date().toISOString() : c.fechaRespuestaCliente,
          fechaEnviadaArea: nextEstado === EstadoCotizacion.PENDIENTE_AREA_MEDICA ? new Date().toISOString() : c.fechaEnviadaArea,
          fechaAprobacionArea: nextEstado === EstadoCotizacion.APROBADA_AREA_MEDICA ? new Date().toISOString() : c.fechaAprobacionArea,
          fechaProgramacion: nextEstado === EstadoCotizacion.PROGRAMADA ? new Date().toISOString() : c.fechaProgramacion,
          fechaOcSolicitada: nextEstado === EstadoCotizacion.OC_SOLICITADA ? new Date().toISOString() : c.fechaOcSolicitada,
          fechaOcRecibida: nextEstado === EstadoCotizacion.OC_RECIBIDA ? new Date().toISOString() : c.fechaOcRecibida,
          fechaFacturacion: nextEstado === EstadoCotizacion.FACTURADA ? new Date().toISOString() : c.fechaFacturacion,
          fechaPago: nextEstado === EstadoCotizacion.PAGADA ? new Date().toISOString() : c.fechaPago,
        };
      }
      return c;
    });

    setCotizaciones(updated);
    if (selectedCotizacion?.id === cotId) {
      setSelectedCotizacion(updated.find((c) => c.id === cotId) || null);
    }

    registrarHistorial(
      `Cambio de Estado: ${targetCot.estado} ➔ ${nextEstado}`,
      'cotizacion',
      cotId,
      `Cotización ${targetCot.numeroCotizacion} actualizada por el operador.`
    );

    // Auto side-effects for specific state transitions
    if (nextEstado === EstadoCotizacion.PROGRAMADA) {
      // Create scheduling record
      const newProg: Programacion = {
        id: Date.now(),
        cotizacionId: cotId,
        eventoId: targetCot.eventos[0]?.id || 1,
        fechaProgramada: targetCot.eventos[0]?.fecha || new Date().toISOString().split('T')[0],
        horaInicio: targetCot.eventos[0]?.horaInicio || '08:00',
        horaFin: targetCot.eventos[0]?.horaFin || '17:00',
        recursoAsignado: 'Ambulancia TAB-01 + Paramedico Asignado',
        outlookEventId: `OUTLOOK-SYNC-${Math.floor(Math.random() * 100000)}`,
        estado: 'CONFIRMADA',
      };
      setProgramaciones((prev) => [...prev, newProg]);
    }

    if (nextEstado === EstadoCotizacion.OC_SOLICITADA) {
      const newOc: OrdenCompra = {
        id: Date.now(),
        cotizacionId: cotId,
        fechaSolicitud: new Date().toISOString(),
        estado: 'SOLICITADA',
      };
      setOrdenesCompra((prev) => [...prev, newOc]);
    }

    if (nextEstado === EstadoCotizacion.PENDIENTE_FACTURACION) {
      const newFact: Factura = {
        id: Date.now(),
        cotizacionId: cotId,
        numeroFactura: `FACT-2026-${Math.floor(1000 + Math.random() * 9000)}`,
        fechaFacturacion: new Date().toISOString().split('T')[0],
        fechaVencimiento: new Date(Date.now() + 30 * 86400000).toISOString().split('T')[0],
        valorFacturado: targetCot.valorTotal,
        estado: 'PENDIENTE',
      };
      setFacturas((prev) => [...prev, newFact]);
    }
  };

  // Add Event to Quotation
  const handleAddEvento = (cotId: number, rawEvento: Partial<Evento>) => {
    const targetCot = cotizaciones.find((c) => c.id === cotId);
    if (!targetCot) return;

    const targetCliente = clientes.find((cl) => cl.id === targetCot.clienteId) || null;
    const calc = calcularEvento(rawEvento, targetCliente, festivos, tarifas);

    const newEv: Evento = {
      id: Date.now(),
      cotizacionId: cotId,
      servicioId: rawEvento.servicioId || 1,
      fecha: rawEvento.fecha || new Date().toISOString().split('T')[0],
      horaInicio: rawEvento.horaInicio || '08:00',
      horaFin: rawEvento.horaFin || '17:00',
      ciudadId: rawEvento.ciudadId || 1,
      direccion: rawEvento.direccion || 'Sede Principal',
      contacto: rawEvento.contacto || 'Contacto Directo',
      telefono: rawEvento.telefono || '300-000-0000',
      tipoDia: calc.tipoDia,
      horasDiurnas: calc.horasDiurnas,
      horasNocturnas: calc.horasNocturnas,
      valorHorasDiurnas: calc.valorHorasDiurnas,
      valorHorasNocturnas: calc.valorHorasNocturnas,
      valorExtras: calc.valorExtras,
      valorEvento: calc.valorEvento,
      orden: targetCot.eventos.length + 1,
      extras: rawEvento.extras || [],
    };

    const updatedEventos = [...targetCot.eventos, newEv];
    const newSubtotal = updatedEventos.reduce((s, e) => s + e.valorHorasDiurnas + e.valorHorasNocturnas, 0);
    const newExtras = updatedEventos.reduce((s, e) => s + e.valorExtras, 0);
    const newTotal = newSubtotal + newExtras;

    const updatedCots = cotizaciones.map((c) => {
      if (c.id === cotId) {
        return {
          ...c,
          eventos: updatedEventos,
          valorSubtotal: newSubtotal,
          valorExtras: newExtras,
          valorTotal: newTotal,
          estado: c.estado === EstadoCotizacion.BORRADOR ? EstadoCotizacion.COTIZADA : c.estado,
        };
      }
      return c;
    });

    setCotizaciones(updatedCots);
    if (selectedCotizacion?.id === cotId) {
      setSelectedCotizacion(updatedCots.find((c) => c.id === cotId) || null);
    }

    registrarHistorial(
      'Evento Agregado a Cotización',
      'cotizacion',
      cotId,
      `Evento de servicio #${newEv.servicioId} por $${newEv.valorEvento.toLocaleString('es-CO')} COP.`
    );
  };

  const handleDeleteEvento = (cotId: number, eventoId: number) => {
    const targetCot = cotizaciones.find((c) => c.id === cotId);
    if (!targetCot) return;

    const updatedEventos = targetCot.eventos.filter((e) => e.id !== eventoId);
    const newSubtotal = updatedEventos.reduce((s, e) => s + e.valorHorasDiurnas + e.valorHorasNocturnas, 0);
    const newExtras = updatedEventos.reduce((s, e) => s + e.valorExtras, 0);
    const newTotal = newSubtotal + newExtras;

    const updatedCots = cotizaciones.map((c) => {
      if (c.id === cotId) {
        return {
          ...c,
          eventos: updatedEventos,
          valorSubtotal: newSubtotal,
          valorExtras: newExtras,
          valorTotal: newTotal,
        };
      }
      return c;
    });

    setCotizaciones(updatedCots);
    if (selectedCotizacion?.id === cotId) {
      setSelectedCotizacion(updatedCots.find((c) => c.id === cotId) || null);
    }
  };

  const handleCreateCotizacion = (clienteId: number, contactoId?: number, observaciones?: string) => {
    const numSeq = cotizaciones.length + 49; // COT-2026-00XX
    const newCot: Cotizacion = {
      id: Date.now(),
      numeroCotizacion: `COT-2026-00${numSeq}`,
      clienteId,
      contactoId,
      estado: EstadoCotizacion.BORRADOR,
      usuarioCreadorId: 1,
      fechaCreacion: new Date().toISOString(),
      valorSubtotal: 0,
      valorExtras: 0,
      valorTotal: 0,
      observaciones,
      condicionesComerciales: config.pdfCondicionesGenerales,
      eventos: [],
    };

    setCotizaciones([newCot, ...cotizaciones]);
    setSelectedCotizacion(newCot);

    registrarHistorial(
      'Nueva Cotización Creada',
      'cotizacion',
      newCot.id,
      `Borrador ${newCot.numeroCotizacion} creado para el cliente ID #${clienteId}`
    );
  };

  // Filter cotizaciones by search query if set
  const filteredCotizaciones = searchQuery
    ? cotizaciones.filter(
        (c) =>
          c.numeroCotizacion.toLowerCase().includes(searchQuery.toLowerCase()) ||
          clientes.find((cl) => cl.id === c.clienteId)?.empresa.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : cotizaciones;

  return (
    <div className="min-h-screen bg-slate-100 flex text-slate-900 font-sans antialiased">
      {/* Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={(tab) => {
          setActiveTab(tab);
          setSelectedCotizacion(null);
        }}
        collapsed={sidebarCollapsed}
        setCollapsed={setSidebarCollapsed}
        alertCount={alertas.filter((a) => a.activa && !a.fechaVisto).length}
      />

      {/* Main Container */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Topbar */}
        <Topbar
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          alertas={alertas}
          onMarkAsRead={(id) =>
            setAlertas(alertas.map((a) => (a.id === id ? { ...a, fechaVisto: new Date().toISOString() } : a)))
          }
          onNavigateToAlert={(alerta) => {
            setActiveTab('alertas');
          }}
          onNewQuotation={() => {
            setActiveTab('cotizaciones');
          }}
        />

        {/* Dynamic Tab Content */}
        <main className="flex-1 overflow-y-auto p-6 max-w-7xl w-full mx-auto space-y-6">
          {selectedCotizacion ? (
            <CotizacionDetailView
              cotizacion={selectedCotizacion}
              cliente={clientes.find((c) => c.id === selectedCotizacion.clienteId)}
              contacto={contactos.find((ct) => ct.id === selectedCotizacion.contactoId)}
              servicios={INITIAL_SERVICIOS}
              ciudades={INITIAL_CIUDADES}
              festivos={festivos}
              tarifas={tarifas}
              config={config}
              onBack={() => setSelectedCotizacion(null)}
              onStateTransition={handleStateTransition}
              onAddEvento={handleAddEvento}
              onDeleteEvento={handleDeleteEvento}
              onDuplicateEvento={(cotId, evId) => {
                const ev = selectedCotizacion.eventos.find((e) => e.id === evId);
                if (ev) handleAddEvento(cotId, ev);
              }}
            />
          ) : (
            <>
              {activeTab === 'dashboard' && (
                <DashboardView
                  cotizaciones={filteredCotizaciones}
                  clientes={clientes}
                  alertas={alertas}
                  historial={historial}
                  onNavigateTab={setActiveTab}
                  onSelectCotizacion={setSelectedCotizacion}
                />
              )}

              {activeTab === 'clientes' && (
                <ClientesView
                  clientes={clientes}
                  contactos={contactos}
                  interacciones={interacciones}
                  tareas={tareas}
                  ciudades={INITIAL_CIUDADES}
                  onAddCliente={(n) => {
                    const c: Cliente = {
                      id: Date.now(),
                      empresa: n.empresa || '',
                      nit: n.nit || '',
                      correoPrincipal: n.correoPrincipal || '',
                      telefonoPrincipal: n.telefonoPrincipal || '',
                      tipoCliente: n.tipoCliente || INITIAL_CLIENTES[0].tipoCliente,
                      sector: n.sector,
                      ciudadId: n.ciudadId || 1,
                      direccion: n.direccion,
                      activo: true,
                      fechaCreacion: new Date().toISOString(),
                      usuarioCreadorId: 1,
                    };
                    setClientes([c, ...clientes]);
                  }}
                  onAddContacto={(ct) => setContactos([{ id: Date.now(), ...ct } as any, ...contactos])}
                  onAddInteraccion={(it) => setInteracciones([{ id: Date.now(), ...it } as any, ...interacciones])}
                  onAddTarea={(t) => setTareas([{ id: Date.now(), ...t } as any, ...tareas])}
                />
              )}

              {activeTab === 'tarifas' && (
                <TarifasView
                  tarifas={tarifas}
                  ciudades={INITIAL_CIUDADES}
                  servicios={INITIAL_SERVICIOS}
                  clientes={clientes}
                  onAddTarifa={(nt) => setTarifas([{ id: Date.now(), ...nt } as any, ...tarifas])}
                />
              )}

              {activeTab === 'cotizaciones' && (
                <CotizacionesView
                  cotizaciones={filteredCotizaciones}
                  clientes={clientes}
                  contactos={contactos}
                  onSelectCotizacion={setSelectedCotizacion}
                  onStateTransition={handleStateTransition}
                  onCreateCotizacion={handleCreateCotizacion}
                />
              )}

              {activeTab === 'programacion' && (
                <ProgramacionView
                  programaciones={programaciones}
                  cotizaciones={cotizaciones}
                  clientes={clientes}
                  onSyncOutlook={() =>
                    alert('Sincronización completa con Microsoft Outlook Calendar.')
                  }
                />
              )}

              {activeTab === 'areas' && (
                <AreasMedicasView
                  areasMedicas={areasMedicas}
                  cotizaciones={cotizaciones}
                  clientes={clientes}
                  onApproveAreaMedica={(cotId) =>
                    handleStateTransition(cotId, EstadoCotizacion.APROBADA_AREA_MEDICA)
                  }
                  onRejectAreaMedica={(cotId) =>
                    handleStateTransition(cotId, EstadoCotizacion.RECHAZADA_CLIENTE)
                  }
                />
              )}

              {activeTab === 'ordenes' && (
                <OrdenesCompraView
                  ordenes={ordenesCompra}
                  cotizaciones={cotizaciones}
                  clientes={clientes}
                  onReceiveOC={(ocId, numOc) => {
                    setOrdenesCompra(
                      ordenesCompra.map((o) =>
                        o.id === ocId ? { ...o, numeroOc: numOc, estado: 'RECIBIDA' } : o
                      )
                    );
                    const targetOc = ordenesCompra.find((o) => o.id === ocId);
                    if (targetOc) handleStateTransition(targetOc.cotizacionId, EstadoCotizacion.OC_RECIBIDA);
                  }}
                />
              )}

              {activeTab === 'facturacion' && (
                <FacturacionView
                  facturas={facturas}
                  cotizaciones={cotizaciones}
                  clientes={clientes}
                  onAddFactura={(f) => setFacturas([{ id: Date.now(), ...f } as any, ...facturas])}
                  onPayFactura={(fId) => {
                    setFacturas(
                      facturas.map((f) =>
                        f.id === fId ? { ...f, estado: 'PAGADA', fechaPago: new Date().toISOString() } : f
                      )
                    );
                    const targetF = facturas.find((f) => f.id === fId);
                    if (targetF) handleStateTransition(targetF.cotizacionId, EstadoCotizacion.PAGADA);
                  }}
                />
              )}

              {activeTab === 'alertas' && (
                <AlertasView
                  alertas={alertas}
                  onMarkAsRead={(id) =>
                    setAlertas(alertas.map((a) => (a.id === id ? { ...a, fechaVisto: new Date().toISOString() } : a)))
                  }
                />
              )}

              {activeTab === 'historial' && <HistorialView historial={historial} />}

              {activeTab === 'configuracion' && (
                <ConfiguracionView
                  config={config}
                  festivos={festivos}
                  onSaveConfig={setConfig}
                  onAddFestivo={(fecha, nombre) =>
                    setFestivos([
                      ...festivos,
                      { id: Date.now(), fecha, nombre, origen: INITIAL_FESTIVOS[0].origen },
                    ])
                  }
                />
              )}

              {activeTab === 'auditoria' && <PythonAuditView />}
            </>
          )}
        </main>
      </div>
    </div>
  );
}
