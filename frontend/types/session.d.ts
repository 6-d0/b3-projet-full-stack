declare interface ISession {
  pk: int;
  name: string;
  slug: string;
  uuid: string;
  courses: ICourses[];
}

declare type ISessions = Array<ISession>;
