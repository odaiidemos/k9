export const DogStatus = {
  ACTIVE: 'ACTIVE',
  TRAINING: 'TRAINING',
  RETIRED: 'RETIRED',
  INJURED: 'INJURED',
  DECEASED: 'DECEASED',
} as const;

export type DogStatus = typeof DogStatus[keyof typeof DogStatus];

export const DogGender = {
  MALE: 'MALE',
  FEMALE: 'FEMALE',
} as const;

export type DogGender = typeof DogGender[keyof typeof DogGender];

export interface Dog {
  id: string;
  name: string;
  code: string;
  breed: string;
  family_line?: string;
  gender: DogGender;
  birth_date: string;
  microchip_id?: string;
  current_status: DogStatus;
  location?: string;
  specialization?: string;
  color?: string;
  weight?: number;
  height?: number;
  birth_certificate?: string;
  photo?: string;
  medical_records: string[];
  assigned_to_user_id?: string;
  father_id?: string;
  mother_id?: string;
  created_at: string;
  updated_at?: string;
}

export interface DogCreate {
  name: string;
  code: string;
  breed: string;
  family_line?: string;
  gender: DogGender;
  birth_date: string;
  microchip_id?: string;
  current_status?: DogStatus;
  location?: string;
  specialization?: string;
  color?: string;
  weight?: number;
  height?: number;
  birth_certificate?: string;
  photo?: string;
  medical_records?: string[];
  assigned_to_user_id?: string;
  father_id?: string;
  mother_id?: string;
}

export interface DogUpdate {
  name?: string;
  code?: string;
  breed?: string;
  family_line?: string;
  gender?: DogGender;
  birth_date?: string;
  microchip_id?: string;
  current_status?: DogStatus;
  location?: string;
  specialization?: string;
  color?: string;
  weight?: number;
  height?: number;
  birth_certificate?: string;
  photo?: string;
  medical_records?: string[];
  assigned_to_user_id?: string;
  father_id?: string;
  mother_id?: string;
}

export interface DogFilters {
  skip?: number;
  limit?: number;
  status?: DogStatus;
  gender?: DogGender;
  breed?: string;
  search?: string;
}

export interface PaginatedDogs {
  items: Dog[];
  total: number;
  skip: number;
  limit: number;
}

export interface DogStatistics {
  total: number;
  by_status: Record<string, number>;
  by_gender: Record<string, number>;
  by_breed: Record<string, number>;
  top_breeds: [string, number][];
}
