declare interface ISchedules {
  pk: number;
  uuid: string;
  date: Date;
  can_subscribe: boolean;
  can_subscribe_until: Date?;
  classroom: string;
  teacher: IUser;
  session: ISession;
}
