export class Agent {
  public fatigue_level: string;
  public stress_level: string;
  public daily_obligations: string[];

  constructor(
    fatigue_level: string,
    stress_level: string,
    daily_obligations: string[]
  ) {
    this.fatigue_level = fatigue_level;
    this.stress_level = stress_level;
    this.daily_obligations = daily_obligations;
  }
}

export class AgentGet {
  predicted_session_duration: string;

  constructor(predicted_session_duration: string) {
    this.predicted_session_duration = predicted_session_duration;
  }
}
