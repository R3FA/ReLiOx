import { AgentDailyObligationFlaskFormat } from '../DailyObligation/DailyObligationGetModel';

export class Agent {
  public start_time: string;
  public end_time: string;
  public session_duration: number;
  public fatigue_level: string;
  public stress_level: string;
  public daily_obligations_count: number;
  public daily_obligations: AgentDailyObligationFlaskFormat[];

  constructor(
    start_time: string,
    end_time: string,
    session_duration: number,
    fatigue_level: string,
    stress_level: string,
    daily_obligations_count: number,
    daily_obligations: AgentDailyObligationFlaskFormat[]
  ) {
    this.start_time = start_time;
    this.end_time = end_time;
    this.session_duration = session_duration;
    this.fatigue_level = fatigue_level;
    this.stress_level = stress_level;
    this.daily_obligations_count = daily_obligations_count;
    this.daily_obligations = daily_obligations.map(
      (obligation) =>
        new AgentDailyObligationFlaskFormat(obligation.daily_obligation_type)
    );
  }
}

export class AgentPost {
  public data: Agent[];

  constructor(data: Agent[]) {
    this.data = data;
  }
}

export class AgentGet {
  predicted_session_duration: string;

  constructor(predicted_session_duration: string) {
    this.predicted_session_duration = predicted_session_duration;
  }
}
