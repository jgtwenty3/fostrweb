export enum Role {
	owner = "Owner",
	worker = "Worker",
	foster = "Foster",
	transporter = "Transporter",
	user = "User",
  }
  
  // Define the User type with the role as Role
  export interface User {
	id: number;
	name: string;
	email: string;
	role: Role; // Role now refers to the Role enum type
  }
  