export interface ClaimMovement {
  idCarvajal: number;
  claimNumber: string;
  identificationNumber: string;
  productCode: string;
  planCode: string;
  coverage: string;
  branchCode: string;
  movementValue: number;
  movementDate: string;
  movementType: string;
  partner: string;
  cardifId: string;
  claimKey: string;
  partnerCode: number;
  claimStatus: string;
  majorStatus: string;
  channel: string;
  pandemic: string;
  paymentBeneficiary: string;
  coinsuranceType: number;
  retainedCoinsuranceValue: number;
  cededCoinsuranceValue: number;
  birthDate: string;
  occurrenceDate: string;
  partnerNoticeDate: string;
  cardifNoticeDate: string;
}

export interface IndividualNewsRequest {
  idCarvajal: number;
  movementType: string;
  partner: string;
  coverage: string;
  cardifId: string;
  claimKey: string;
  branchCode: string;
  claimNumber: string;
  partnerCode: number;
  claimStatus: string;
  majorStatus: string;
  channel: string;
  pandemic: string;
  justification: string;
  paymentBeneficiary: string | null;
  coinsuranceType: number | null;
  retainedCoinsuranceValue: number | null;
  cededCoinsuranceValue: number | null;
  birthDate: string | null;
  occurrenceDate: string | null;
  partnerNoticeDate: string | null;
  cardifNoticeDate: string | null;
}

export interface IndividualNewsDeleteRequest {
  idCarvajal: number;
  justification: string;
}

export interface IndividualNews {
  code: number;
  idCarvajal: number;
  claimNumber: string;
  newsType: string;
  status: string;
  justification: string;
  processDate: string;
  requestUser: string;
  authorizerUser: string;
}