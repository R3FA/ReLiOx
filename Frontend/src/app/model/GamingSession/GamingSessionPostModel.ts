export class GamingSessionPostFlaskFormat {
  public user_id: number;
  public event_date: string;
  public fatigue_level: string;
  public stress_level: string;
  public daily_obligations: string[];

  constructor(
    user_id: number,
    eventDate: string,
    fatigueLevel: string,
    stressLevel: string,
    dailyObligations: string[]
  ) {
    this.user_id = user_id;
    this.event_date = eventDate;
    this.fatigue_level = fatigueLevel;
    this.stress_level = stressLevel;
    this.daily_obligations = dailyObligations;
  }
}

export enum FatigueLevel {
  VERY_LOW_FATIGUE = 'VERY_LOW_FATIGUE',
  LOW_FATIGUE = 'LOW_FATIGUE',
  MODERATE_FATIGUE = 'MODERATE_FATIGUE',
  HIGH_FATIGUE = 'HIGH_FATIGUE',
  VERY_HIGH_FATIGUE = 'VERY_HIGH_FATIGUE',
}

export enum StressLevel {
  VERY_LOW_STRESS = 'VERY_LOW_STRESS',
  LOW_STRESS = 'LOW_STRESS',
  MODERATE_STRESS = 'MODERATE_STRESS',
  HIGH_STRESS = 'HIGH_STRESS',
  VERY_HIGH_STRESS = 'VERY_HIGH_STRESS',
}
