import {
  AreaMedica,
  Ciudad,
  Cliente,
  ConfiguracionSistema,
  ContactoCliente,
  Cotizacion,
  Factura,
  Festivo,
  HistorialActividad,
  InteraccionCRM,
  OrdenCompra,
  OrigenFestivo,
  PrioridadTarea,
  Programacion,
  Servicio,
  Tarea,
  Tarifa,
  TipoAlerta,
  TipoCliente,
  TipoDia,
  TipoExtra,
  TipoHorario,
  TipoInteraccionCRM,
  TipoServicio,
  Usuario,
  Alerta,
  EstadoCotizacion,
} from '../types';

export const INITIAL_USUARIOS: Usuario[] = [
  {
    id: 1,
    nombre: 'Administrador General',
    email: 'admin@medicosne.com.co',
    activo: true,
    fechaCreacion: '2026-01-01T08:00:00Z',
  },
  {
    id: 2,
    nombre: 'Ejecutivo Comercial - Carlos',
    email: 'carlos.comercial@medicosne.com.co',
    activo: true,
    fechaCreacion: '2026-01-15T09:30:00Z',
  },
  {
    id: 3,
    nombre: 'Coordinadora Médica - Dr. Elena',
    email: 'elena.medica@medicosne.com.co',
    activo: true,
    fechaCreacion: '2026-02-01T10:00:00Z',
  },
];

export const INITIAL_CIUDADES: Ciudad[] = [
  { id: 1, nombre: 'Bogotá, D.C.', departamento: 'Cundinamarca', activo: true },
  { id: 2, nombre: 'Medellín', departamento: 'Antioquia', activo: true },
  { id: 3, nombre: 'Cali', departamento: 'Valle del Cauca', activo: true },
  { id: 4, nombre: 'Barranquilla', departamento: 'Atlántico', activo: true },
  { id: 5, nombre: 'Bucaramanga', departamento: 'Santander', activo: true },
];

export const INITIAL_SERVICIOS: Servicio[] = [
  { id: 1, codigo: 'SERV-TAB', nombre: 'Ambulancia TAB (Soporte Básico)', tipo: TipoServicio.AMBULANCIA_TAB, activo: true },
  { id: 2, codigo: 'SERV-TAM', nombre: 'Ambulancia TAM (Soporte Medicalizado)', tipo: TipoServicio.AMBULANCIA_TAM, activo: true },
  { id: 3, codigo: 'SERV-AUX', nombre: 'Auxiliar de Enfermería de Acompañamiento', tipo: TipoServicio.AUXILIAR_ENFERMERIA, activo: true },
  { id: 4, codigo: 'SERV-PAR', nombre: 'Paramédico Operativo de Campo', tipo: TipoServicio.PARAMEDICO, activo: true },
  { id: 5, codigo: 'SERV-MED', nombre: 'Médico General de Evento/Turno', tipo: TipoServicio.MEDICO_GENERAL, activo: true },
  { id: 6, codigo: 'SERV-CTAB', nombre: 'Conductor Certificado TAB', tipo: TipoServicio.CONDUCTOR_TAB, activo: true },
  { id: 7, codigo: 'SERV-CTAM', nombre: 'Conductor Certificado TAM', tipo: TipoServicio.CONDUCTOR_TAM, activo: true },
];

export const INITIAL_CLIENTES: Cliente[] = [
  {
    id: 1,
    empresa: 'Hospital El Bosque S.A.',
    nit: '890.123.456-7',
    correoPrincipal: 'compras@bosque.com.co',
    telefonoPrincipal: '601-234-5678',
    tipoCliente: TipoCliente.ESPECIAL,
    sector: 'Salud / Hospitalario',
    ciudadId: 1,
    direccion: 'Cra. 7 # 134-20, Bogotá',
    sitioWeb: 'https://hospitalelbosque.com.co',
    observaciones: 'Cliente institucional preferencial con tarifas negociadas por contrato 2026.',
    activo: true,
    fechaCreacion: '2026-01-10T11:00:00Z',
    usuarioCreadorId: 1,
  },
  {
    id: 2,
    empresa: 'Clínica Palermo',
    nit: '900.234.567-1',
    correoPrincipal: 'recepcion@palermo.com.co',
    telefonoPrincipal: '601-345-6789',
    tipoCliente: TipoCliente.NORMAL,
    sector: 'Salud / Clínica Privada',
    ciudadId: 1,
    direccion: 'Calle 45 # 22-02, Bogotá',
    sitioWeb: 'https://clinicapalermo.com.co',
    observaciones: 'Servicios de traslado asistencial para pacientes remitidos.',
    activo: true,
    fechaCreacion: '2026-02-05T09:15:00Z',
    usuarioCreadorId: 2,
  },
  {
    id: 3,
    empresa: 'SOS Médico S.A.S.',
    nit: '800.345.678-2',
    correoPrincipal: 'operaciones@sosmedico.com',
    telefonoPrincipal: '604-456-7890',
    tipoCliente: TipoCliente.ESPECIAL,
    sector: 'Medicina Prepagada / ARL',
    ciudadId: 2,
    direccion: 'Av. El Poblado # 10-50, Medellín',
    sitioWeb: 'https://sosmedico.com',
    observaciones: 'Cobertura de eventos masivos e industriales en Antioquia.',
    activo: true,
    fechaCreacion: '2026-03-01T14:20:00Z',
    usuarioCreadorId: 2,
  },
];

export const INITIAL_CONTACTOS: ContactoCliente[] = [
  { id: 1, clienteId: 1, nombre: 'Carlos Mendoza', cargo: 'Jefe de Compras y Suministros', correo: 'cmendoza@bosque.com.co', telefono: '301-234-5678', esPrincipal: true, activo: true },
  { id: 2, clienteId: 1, nombre: 'Dra. Laura Gómez', cargo: 'Coordinadora de Urgencias', correo: 'lgomez@bosque.com.co', telefono: '302-345-6789', esPrincipal: false, activo: true },
  { id: 3, clienteId: 2, nombre: 'Ing. Roberto Silva', cargo: 'Director Operativo', correo: 'rsilva@palermo.com.co', telefono: '310-456-7890', esPrincipal: true, activo: true },
  { id: 4, clienteId: 3, nombre: 'María Paula Ríos', cargo: 'Gestora de Contratos', correo: 'mrios@sosmedico.com', telefono: '315-567-8901', esPrincipal: true, activo: true },
];

export const INITIAL_INTERACCIONES: InteraccionCRM[] = [
  { id: 1, clienteId: 1, cotizacionId: 1, tipo: TipoInteraccionCRM.LLAMADA, fechaHora: '2026-07-20T10:30:00Z', asunto: 'Seguimiento a solicitud de Orden de Compra', descripcion: 'Carlos confirmó que la OC está en firma en la gerencia financiera.', usuarioId: 2 },
  { id: 2, clienteId: 1, cotizacionId: 1, tipo: TipoInteraccionCRM.EMAIL, fechaHora: '2026-07-18T16:00:00Z', asunto: 'Envío de propuesta económica revisada', descripcion: 'Se adjuntó PDF con desglose de evento TAB + TAM para evento institucional.', usuarioId: 2 },
  { id: 3, clienteId: 2, tipo: TipoInteraccionCRM.REUNION, fechaHora: '2026-07-15T11:00:00Z', asunto: 'Reunión de presentación de portafolio 2026', descripcion: 'Se presentaron tarifas diurnas y nocturnas para traslado asistencial.', usuarioId: 1 },
];

export const INITIAL_TAREAS: Tarea[] = [
  { id: 1, clienteId: 1, cotizacionId: 1, titulo: 'Confirmar recepción de Orden de Compra', descripcion: 'Hacer llamada de verificación con Tesorería del Hospital El Bosque.', prioridad: PrioridadTarea.ALTA, fechaVencimiento: '2026-07-22T17:00:00Z', completada: false, usuarioAsignadoId: 2, usuarioCreadorId: 1 },
  { id: 2, clienteId: 2, titulo: 'Enviar propuesta de convenio anual', descripcion: 'Preparar borrador con tarifas especiales para traslados recurrentes.', prioridad: PrioridadTarea.MEDIA, fechaVencimiento: '2026-07-25T12:00:00Z', completada: false, usuarioAsignadoId: 2, usuarioCreadorId: 2 },
];

export const INITIAL_FESTIVOS: Festivo[] = [
  { id: 1, fecha: '2026-01-01', nombre: 'Año Nuevo', origen: OrigenFestivo.LIBRERIA },
  { id: 2, fecha: '2026-01-12', nombre: 'Día de los Reyes Magos', origen: OrigenFestivo.LIBRERIA },
  { id: 3, fecha: '2026-03-23', nombre: 'Día de San José', origen: OrigenFestivo.LIBRERIA },
  { id: 4, fecha: '2026-04-02', nombre: 'Jueves Santo', origen: OrigenFestivo.LIBRERIA },
  { id: 5, fecha: '2026-04-03', nombre: 'Viernes Santo', origen: OrigenFestivo.LIBRERIA },
  { id: 6, fecha: '2026-05-01', nombre: 'Día del Trabajo', origen: OrigenFestivo.LIBRERIA },
  { id: 7, fecha: '2026-05-18', nombre: 'Ascensión del Señor', origen: OrigenFestivo.LIBRERIA },
  { id: 8, fecha: '2026-06-08', nombre: 'Corpus Christi', origen: OrigenFestivo.LIBRERIA },
  { id: 9, fecha: '2026-06-15', nombre: 'Sagrado Corazón', origen: OrigenFestivo.LIBRERIA },
  { id: 10, fecha: '2026-06-29', nombre: 'San Pedro y San Pablo', origen: OrigenFestivo.LIBRERIA },
  { id: 11, fecha: '2026-07-20', nombre: 'Día de la Independencia', origen: OrigenFestivo.LIBRERIA },
  { id: 12, fecha: '2026-08-07', nombre: 'Batalla de Boyacá', origen: OrigenFestivo.LIBRERIA },
  { id: 13, fecha: '2026-08-17', nombre: 'La Asunción de la Virgen', origen: OrigenFestivo.LIBRERIA },
  { id: 14, fecha: '2026-10-12', nombre: 'Día de la Raza', origen: OrigenFestivo.LIBRERIA },
  { id: 15, fecha: '2026-11-02', nombre: 'Todos los Santos', origen: OrigenFestivo.LIBRERIA },
  { id: 16, fecha: '2026-11-16', nombre: 'Independencia de Cartagena', origen: OrigenFestivo.LIBRERIA },
  { id: 17, fecha: '2026-12-08', nombre: 'Inmaculada Concepción', origen: OrigenFestivo.LIBRERIA },
  { id: 18, fecha: '2026-12-25', nombre: 'Navidad', origen: OrigenFestivo.LIBRERIA },
];

export const INITIAL_TARIFAS: Tarifa[] = [
  // General Bogotá
  { id: 1, ciudadId: 1, servicioId: 1, tipoDia: TipoDia.ORDINARIO, tipoHorario: TipoHorario.DIURNO, clienteId: null, valorHora: 320000, vigenteDesde: '2026-01-01', activo: true },
  { id: 2, ciudadId: 1, servicioId: 1, tipoDia: TipoDia.ORDINARIO, tipoHorario: TipoHorario.NOCTURNO, clienteId: null, valorHora: 370000, vigenteDesde: '2026-01-01', activo: true },
  { id: 3, ciudadId: 1, servicioId: 1, tipoDia: TipoDia.FESTIVO, tipoHorario: TipoHorario.DIURNO, clienteId: null, valorHora: 420000, vigenteDesde: '2026-01-01', activo: true },
  { id: 4, ciudadId: 1, servicioId: 1, tipoDia: TipoDia.FESTIVO, tipoHorario: TipoHorario.NOCTURNO, clienteId: null, valorHora: 480000, vigenteDesde: '2026-01-01', activo: true },

  { id: 5, ciudadId: 1, servicioId: 2, tipoDia: TipoDia.ORDINARIO, tipoHorario: TipoHorario.DIURNO, clienteId: null, valorHora: 480000, vigenteDesde: '2026-01-01', activo: true },
  { id: 6, ciudadId: 1, servicioId: 2, tipoDia: TipoDia.ORDINARIO, tipoHorario: TipoHorario.NOCTURNO, clienteId: null, valorHora: 550000, vigenteDesde: '2026-01-01', activo: true },

  // Tarifa Especial Hospital El Bosque (clienteId = 1)
  { id: 7, ciudadId: 1, servicioId: 1, tipoDia: TipoDia.ORDINARIO, tipoHorario: TipoHorario.DIURNO, clienteId: 1, valorHora: 280000, vigenteDesde: '2026-01-01', activo: true },
  { id: 8, ciudadId: 1, servicioId: 1, tipoDia: TipoDia.ORDINARIO, tipoHorario: TipoHorario.NOCTURNO, clienteId: 1, valorHora: 330000, vigenteDesde: '2026-01-01', activo: true },
];

export const INITIAL_COTIZACIONES: Cotizacion[] = [
  {
    id: 1,
    numeroCotizacion: 'COT-2026-0048',
    clienteId: 1,
    contactoId: 1,
    estado: EstadoCotizacion.OC_SOLICITADA,
    usuarioCreadorId: 1,
    fechaCreacion: '2026-07-10T09:00:00Z',
    fechaEnviadaCliente: '2026-07-11T14:30:00Z',
    fechaRespuestaCliente: '2026-07-14T11:00:00Z',
    fechaEnviadaArea: '2026-07-14T15:00:00Z',
    fechaAprobacionArea: '2026-07-15T09:30:00Z',
    fechaProgramacion: '2026-07-16T10:00:00Z',
    fechaOcSolicitada: '2026-07-17T11:20:00Z',
    valorSubtotal: 4530000,
    valorExtras: 70000,
    valorTotal: 4600000,
    observaciones: 'Servicio de prevención y respuesta rápida para simulacro institucional.',
    condicionesComerciales: 'Pago a 30 días previa presentación de factura y OC correspondiente.',
    eventos: [
      {
        id: 1,
        cotizacionId: 1,
        servicioId: 1,
        fecha: '2026-07-25',
        horaInicio: '14:00',
        horaFin: '20:00',
        ciudadId: 1,
        direccion: 'Cra. 7 # 134-20 (Edificio Principal)',
        contacto: 'Carlos Mendoza',
        telefono: '301-234-5678',
        tipoDia: TipoDia.ORDINARIO,
        horasDiurnas: 5.0,
        horasNocturnas: 1.0,
        valorHorasDiurnas: 1400000, // 5h x 280.000
        valorHorasNocturnas: 330000, // 1h x 330.000
        valorExtras: 70000,
        valorEvento: 1800000,
        orden: 1,
        extras: [
          { id: 1, tipo: TipoExtra.PEAJE, descripcion: 'Peaje Autopista Norte', valor: 70000 },
        ],
      },
      {
        id: 2,
        cotizacionId: 1,
        servicioId: 2,
        fecha: '2026-07-25',
        horaInicio: '08:00',
        horaFin: '13:00',
        ciudadId: 1,
        direccion: 'Cra. 7 # 134-20',
        contacto: 'Dra. Laura Gómez',
        telefono: '302-345-6789',
        tipoDia: TipoDia.ORDINARIO,
        horasDiurnas: 5.0,
        horasNocturnas: 0,
        valorHorasDiurnas: 2800000,
        valorHorasNocturnas: 0,
        valorExtras: 0,
        valorEvento: 2800000,
        orden: 2,
        extras: [],
      },
    ],
  },
  {
    id: 2,
    numeroCotizacion: 'COT-2026-0051',
    clienteId: 2,
    contactoId: 3,
    estado: EstadoCotizacion.COTIZADA,
    usuarioCreadorId: 2,
    fechaCreacion: '2026-07-19T10:00:00Z',
    valorSubtotal: 2270000,
    valorExtras: 50000,
    valorTotal: 2320000,
    observaciones: 'Traslado asistencial programado para fin de semana.',
    condicionesComerciales: 'Validez de la oferta: 15 días hábiles.',
    eventos: [
      {
        id: 3,
        cotizacionId: 2,
        servicioId: 1,
        fecha: '2026-07-26',
        horaInicio: '08:00',
        horaFin: '13:00',
        ciudadId: 1,
        direccion: 'Calle 45 # 22-02',
        contacto: 'Ing. Roberto Silva',
        telefono: '310-456-7890',
        tipoDia: TipoDia.FESTIVO, // Domingo
        horasDiurnas: 5.0,
        horasNocturnas: 0,
        valorHorasDiurnas: 2100000, // 5 x 420.000
        valorHorasNocturnas: 0,
        valorExtras: 50000,
        valorEvento: 2150000,
        orden: 1,
        extras: [
          { id: 2, tipo: TipoExtra.TRANSPORTE, descripcion: 'Recargo zona rural', valor: 50000 },
        ],
      },
    ],
  },
  {
    id: 3,
    numeroCotizacion: 'COT-2026-0052',
    clienteId: 3,
    contactoId: 4,
    estado: EstadoCotizacion.BORRADOR,
    usuarioCreadorId: 2,
    fechaCreacion: '2026-07-21T08:30:00Z',
    valorSubtotal: 0,
    valorExtras: 0,
    valorTotal: 0,
    observaciones: 'Borrador inicial para evento masivo en Medellín.',
    condicionesComerciales: 'Sujeto a aprobación médica de disponibilidades.',
    eventos: [],
  },
];

export const INITIAL_AREAS_MEDICAS: AreaMedica[] = [
  { id: 1, nombre: 'Área Médica - Coordinación Bogotá', correoContacto: 'coordinacion.bogota@medicosne.com.co', telefono: '601-555-0101', responsable: 'Dra. Elena Martínez', activo: true },
  { id: 2, nombre: 'Área Médica - Coordinación Antioquia', correoContacto: 'coordinacion.medellin@medicosne.com.co', telefono: '604-555-0102', responsable: 'Dr. Fernando Ríos', activo: true },
];

export const INITIAL_PROGRAMACIONES: Programacion[] = [
  {
    id: 1,
    cotizacionId: 1,
    eventoId: 1,
    fechaProgramada: '2026-07-25',
    horaInicio: '14:00',
    horaFin: '20:00',
    recursoAsignado: 'Ambulancia TAB-04 + Conductor Ramírez + Aux. Castro',
    notas: 'Llegada 15 minutos antes a la portería principal.',
    outlookEventId: 'OUTLOOK-EVENT-99881122',
    estado: 'CONFIRMADA',
  },
];

export const INITIAL_ORDENES_COMPRA: OrdenCompra[] = [
  {
    id: 1,
    cotizacionId: 1,
    numeroOc: 'OC-HEB-2026-889',
    fechaSolicitud: '2026-07-17T11:20:00Z',
    estado: 'SOLICITADA',
  },
];

export const INITIAL_FACTURAS: Factura[] = [];

export const INITIAL_ALERTAS: Alerta[] = [
  {
    id: 1,
    tipo: TipoAlerta.OC_DEMORADA,
    titulo: 'Orden de Compra Pendiente',
    mensaje: 'La cotización COT-2026-0048 cumple 4 días en estado OC_SOLICITADA sin recibir archivo.',
    entidadTipo: 'cotizacion',
    entidadId: 1,
    prioridad: 'ADVERTENCIA',
    fechaCreacion: '2026-07-21T07:00:00Z',
    usuarioId: 1,
    activa: true,
  },
  {
    id: 2,
    tipo: TipoAlerta.TAREA_VENCIDA,
    titulo: 'Tarea Comercial Pendiente',
    mensaje: 'Confirmar recepción de Orden de Compra con Hospital El Bosque vence hoy.',
    entidadTipo: 'tarea',
    entidadId: 1,
    prioridad: 'CRITICA',
    fechaCreacion: '2026-07-21T08:00:00Z',
    usuarioId: 2,
    activa: true,
  },
];

export const INITIAL_HISTORIAL: HistorialActividad[] = [
  {
    id: 1,
    fechaHora: '2026-07-21T08:30:00Z',
    usuarioId: 2,
    entidadTipo: 'cotizacion',
    entidadId: 3,
    accion: 'Cotización creada en estado Borrador',
    detalle: 'Generada para el cliente SOS Médico S.A.S.',
    esAutomatico: false,
  },
  {
    id: 2,
    fechaHora: '2026-07-19T10:00:00Z',
    usuarioId: 2,
    entidadTipo: 'cotizacion',
    entidadId: 2,
    accion: 'Cálculo automático de totales actualizado',
    detalle: 'Evento 1 (Festivo) recalculado con tarifa de domingo.',
    esAutomatico: true,
  },
  {
    id: 3,
    fechaHora: '2026-07-17T11:20:00Z',
    usuarioId: 1,
    entidadTipo: 'cotizacion',
    entidadId: 1,
    accion: 'Cambio de estado: PROGRAMADA -> OC_SOLICITADA',
    detalle: 'Correo de solicitud de Orden de Compra enviado a cmendoza@bosque.com.co',
    esAutomatico: false,
  },
];

export const INITIAL_CONFIGURACION: ConfiguracionSistema = {
  empresaNombre: 'Servicios Médicos NE S.A.S.',
  empresaNit: '900.888.777-3',
  empresaDireccion: 'Calle 100 # 19-61, Oficina 502, Bogotá, Colombia',
  empresaTelefono: '601-700-9000',
  empresaLogoPath: '/resources/icons/logo_ne.png',
  outlookCuentaEmail: 'operaciones@medicosne.com.co',
  pdfCondicionesGenerales:
    '1. Precios expresados en Pesos Colombianos (COP).\n2. Validez de la oferta: 15 días calendario.\n3. Cancelaciones con menos de 12 horas de antelación generarán cobro del 50% del valor del servicio.',
  alertasDiasSinRespuesta: 3,
  alertasDiasOcDemorada: 3,
};
