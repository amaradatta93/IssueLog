export class Register {
    username: string;
    password: string;
    email: string;
}

export class User {
    id: number;
    username: string;
    password: string;
    email: string;
    token?: string;
}