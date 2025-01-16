declare interface ISession {
    pk: int,
    name: string,
    slug: string,
    uuid: string,
}

declare type ISessions = Array<ISession>
