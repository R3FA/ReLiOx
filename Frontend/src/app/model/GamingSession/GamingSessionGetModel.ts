import { DailyObligationGetFlaskFormat } from '../DailyObligation/DailyObligationGetModel';

export class GamingSessionGetFlaskFormat {
  public id: number;
  public user_id: number;
  public event_date: string;
  public start_time: string;
  public end_time: string;
  public session_duration: number;
  public fatigue_level: string;
  public stress_level: string;
  public daily_obligations: DailyObligationGetFlaskFormat[];

  constructor(
    id: number,
    user_id: number,
    event_date: string,
    start_time: string,
    end_time: string,
    session_duration: number,
    fatigue_level: string,
    stress_level: string,
    daily_obligations: DailyObligationGetFlaskFormat[]
  ) {
    this.id = id;
    this.user_id = user_id;
    this.event_date = event_date;
    this.start_time = start_time;
    this.end_time = end_time;
    this.session_duration = session_duration;
    this.fatigue_level = fatigue_level;
    this.stress_level = stress_level;
    this.daily_obligations = daily_obligations;
  }
}

export class GamingSessionGet {
  public id: number;
  public userID: number;
  public eventDate: string;
  public startTime: string;
  public endTime: string;
  public sessionDuration: number;
  public fatigueLevel: string;
  public stressLevel: string;
  public dailyObligations: DailyObligationGetFlaskFormat[];

  constructor(
    id: number,
    userID: number,
    eventDate: string,
    startTime: string,
    endTime: string,
    sessionDuration: number,
    fatigueLevel: string,
    stressLevel: string,
    dailyObligations: DailyObligationGetFlaskFormat[]
  ) {
    this.id = id;
    this.userID = userID;
    this.eventDate = eventDate;
    this.startTime = startTime;
    this.endTime = endTime;
    this.sessionDuration = sessionDuration;
    this.fatigueLevel = fatigueLevel;
    this.stressLevel = stressLevel;
    this.dailyObligations = dailyObligations;
  }
}

export class GamingSessionsGetParameters {
  public eventDate: string;
  public userID: number;

  constructor(eventDate: string, userID: number) {
    this.eventDate = eventDate;
    this.userID = userID;
  }
}

export class GamingSessionsDeleteParameters {
  public sessionID: number;
  public userID: number;

  constructor(sessionID: number, userID: number) {
    this.sessionID = sessionID;
    this.userID = userID;
  }

  public setSessionID(value: number) {
    this.sessionID = value;
  }

  public setUserID(value: number) {
    this.userID = value;
  }
}