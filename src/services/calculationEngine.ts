import {
  Cliente,
  Evento,
  Festivo,
  Tarifa,
  TipoCliente,
  TipoDia,
  TipoHorario,
} from '../types';

/**
 * Motor de Reglas de Negocio - Cálculo de Horas, Tipo de Día y Tarifa Strategy
 */

export interface HorasCalculadas {
  horasDiurnas: number;
  horasNocturnas: number;
}

export interface DetalleCalculoEvento {
  tipoDia: TipoDia;
  horasDiurnas: number;
  horasNocturnas: number;
  tarifaDiurnaValor: number;
  tarifaNocturnaValor: number;
  valorHorasDiurnas: number;
  valorHorasNocturnas: number;
  valorExtras: number;
  valorEvento: number;
}

/**
 * Calcula las horas diurnas (07:00-18:59) y nocturnas (19:00-06:59).
 * Maneja eventos que cruzan la medianoche.
 * Ejemplo: 14:00 -> 20:00 => 5h diurnas (14:00-19:00), 1h nocturna (19:00-20:00).
 */
export function calcularHoras(
  fechaStr: string,
  horaInicioStr: string,
  horaFinStr: string
): HorasCalculadas {
  const [hIni, mIni] = horaInicioStr.split(':').map(Number);
  const [hFin, mFin] = horaFinStr.split(':').map(Number);

  const inicio = new Date(`${fechaStr}T${pad2(hIni)}:${pad2(mIni)}:00`);
  let fin = new Date(`${fechaStr}T${pad2(hFin)}:${pad2(mFin)}:00`);

  // Si la hora de fin es menor o igual a inicio, cruza medianoche (día siguiente)
  if (fin <= inicio) {
    fin.setDate(fin.getDate() + 1);
  }

  let horasDiurnas = 0;
  let horasNocturnas = 0;

  // Recorrer intervalo minuto a minuto (o en bloques) para precisión absoluta
  let cursor = new Date(inicio.getTime());
  const minMs = 60 * 1000;

  while (cursor < fin) {
    const hora = cursor.getHours();
    // DIURNO: 07:00 a 18:59 (hora >= 7 y hora < 19)
    const esDiurno = hora >= 7 && hora < 19;

    if (esDiurno) {
      horasDiurnas += 1 / 60;
    } else {
      horasNocturnas += 1 / 60;
    }

    cursor = new Date(cursor.getTime() + minMs);
  }

  return {
    horasDiurnas: Math.round(horasDiurnas * 100) / 100,
    horasNocturnas: Math.round(horasNocturnas * 100) / 100,
  };
}

/**
 * Determina el tipo de día: FESTIVO si es domingo o está en la tabla de festivos; ORDINARIO en otro caso.
 */
export function determinarTipoDia(fechaStr: string, festivos: Festivo[]): TipoDia {
  const date = new Date(`${fechaStr}T00:00:00`);
  const dayOfWeek = date.getDay(); // 0 = Domingo

  if (dayOfWeek === 0) {
    return TipoDia.FESTIVO;
  }

  const esFestivoManual = festivos.some((f) => f.fecha === fechaStr);
  if (esFestivoManual) {
    return TipoDia.FESTIVO;
  }

  return TipoDia.ORDINARIO;
}

/**
 * Obtiene la tarifa correspondiente según el patrón Strategy (Tarifa Especial con fallback a Tarifa General).
 */
export function obtenerTarifa(
  cliente: Cliente | null,
  ciudadId: number,
  servicioId: number,
  tipoDia: TipoDia,
  tipoHorario: TipoHorario,
  fechaStr: string,
  tarifas: Tarifa[]
): Tarifa | null {
  // 1. Si el cliente es ESPECIAL, buscar tarifa específica activa
  if (cliente && cliente.tipoCliente === TipoCliente.ESPECIAL) {
    const tarifaEspecial = tarifas.find(
      (t) =>
        t.clienteId === cliente.id &&
        t.ciudadId === ciudadId &&
        t.servicioId === servicioId &&
        t.tipoDia === tipoDia &&
        t.tipoHorario === tipoHorario &&
        t.activo &&
        t.vigenteDesde <= fechaStr &&
        (!t.vigenteHasta || t.vigenteHasta >= fechaStr)
    );
    if (tarifaEspecial) {
      return tarifaEspecial;
    }
  }

  // 2. Fallback a Tarifa General (clienteId === null)
  const tarifaGeneral = tarifas.find(
    (t) =>
      t.clienteId === null &&
      t.ciudadId === ciudadId &&
      t.servicioId === servicioId &&
      t.tipoDia === tipoDia &&
      t.tipoHorario === tipoHorario &&
      t.activo &&
      t.vigenteDesde <= fechaStr &&
      (!t.vigenteHasta || t.vigenteHasta >= fechaStr)
  );

  return tarifaGeneral || null;
}

/**
 * Realiza el cálculo integral de un Evento dentro de una Cotización.
 */
export function calcularEvento(
  evento: Partial<Evento>,
  cliente: Cliente | null,
  festivos: Festivo[],
  tarifas: Tarifa[]
): DetalleCalculoEvento {
  const fecha = evento.fecha || new Date().toISOString().split('T')[0];
  const horaInicio = evento.horaInicio || '08:00';
  const horaFin = evento.horaFin || '17:00';
  const ciudadId = evento.ciudadId || 1;
  const servicioId = evento.servicioId || 1;

  // 1. Determinar tipo de día
  const tipoDia = determinarTipoDia(fecha, festivos);

  // 2. Calcular desglose de horas diurnas y nocturnas
  const { horasDiurnas, horasNocturnas } = calcularHoras(fecha, horaInicio, horaFin);

  // 3. Buscar tarifa diurna y nocturna
  const tarifaDiurnaObj = obtenerTarifa(
    cliente,
    ciudadId,
    servicioId,
    tipoDia,
    TipoHorario.DIURNO,
    fecha,
    tarifas
  );

  const tarifaNocturnaObj = obtenerTarifa(
    cliente,
    ciudadId,
    servicioId,
    tipoDia,
    TipoHorario.NOCTURNO,
    fecha,
    tarifas
  );

  const tarifaDiurnaValor = tarifaDiurnaObj ? tarifaDiurnaObj.valorHora : 300000; // Valor fallback por defecto
  const tarifaNocturnaValor = tarifaNocturnaObj ? tarifaNocturnaObj.valorHora : 350000;

  const valorHorasDiurnas = Math.round(horasDiurnas * tarifaDiurnaValor);
  const valorHorasNocturnas = Math.round(horasNocturnas * tarifaNocturnaValor);

  const valorExtras = (evento.extras || []).reduce((sum, ext) => sum + ext.valor, 0);

  const valorEvento = valorHorasDiurnas + valorHorasNocturnas + valorExtras;

  return {
    tipoDia,
    horasDiurnas,
    horasNocturnas,
    tarifaDiurnaValor,
    tarifaNocturnaValor,
    valorHorasDiurnas,
    valorHorasNocturnas,
    valorExtras,
    valorEvento,
  };
}

function pad2(num: number): string {
  return num < 10 ? `0${num}` : `${num}`;
}
