import Axios, { AxiosResponse } from "axios";
type TFilters = Record<string, number | string | object | boolean>;

type THttpOptions = {
  showModal?: boolean;
  showSnackbar?: boolean;
};
type THttpGetListOptions = {
  filters?: TFilters;
} & THttpOptions;
type THttpCreateItemOptions = {
  data?: Record<string, any>;
} & THttpOptions;
type THttpGetOrDeleteItemOptions = {
  id?: number;
} & THttpOptions;
type THttpUpdateItemOptions = THttpCreateItemOptions &
  THttpGetOrDeleteItemOptions;

export declare class http {
  urls: Record<string, string>
  getFilterValues: (filters: TFilters | undefined) => any
  getUrl: (url_name: string, id?: number) => string
  catchError: (error: any, options: THttpOptions) => boolean
  getHeaders: () => Record<string, string>
  async getList: <T>(url_name: string, options?: THttpGetListOptions) => Promise<AxiosResponse<T>>
  async getItem: <T>(url_name: string, options?: THttpGetOrDeleteItemOptions) => Promise<AxiosResponse<T>>
  async createItem: <T>(url_name: string, options: THttpCreateItemOptions) => Promise<AxiosResponse<T>>
  async partialUpdateItem: <T>(url_name: string, options: THttpUpdateItemOptions) => Promise<AxiosResponse<T>>
  async updateItem: <T>(url_name: string, options: THttpUpdateItemOptions) => Promise<AxiosResponse<T>>
  async deleteItem: <T>(url_name: string, options: THttpGetOrDeleteItemOptions) => Promise<AxiosResponse<T>>
};
