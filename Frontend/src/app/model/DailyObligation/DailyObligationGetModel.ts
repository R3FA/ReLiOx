export class DailyObligationGet {
  id: number;
  dailyObligationType: string;

  constructor(id: number, dailyObligationType: string) {
    this.id = id;
    this.dailyObligationType = dailyObligationType;
  }
}

export class DailyObligationGetFlaskFormat {
  id: number;
  daily_obligation_type: string;

  constructor(id: number, daily_obligation_type: string) {
    this.id = id;
    this.daily_obligation_type = daily_obligation_type;
  }
}

export class AgentDailyObligationFlaskFormat {
  daily_obligation_type: string;

  constructor(daily_obligation_type: string) {
    this.daily_obligation_type = daily_obligation_type;
  }
}
