import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react';

export const api = createApi({
  baseQuery: fetchBaseQuery({baseUrl: process.env.REACT_APP_BASE_URL}),
  reducerPath:"adminApi",
  tagTypes:["User", "Products","Customers", "Transactions", "Sales"],
  endpoints: (build)=>({
    getUser: build.query({
      query:(id)=>`users/${id}`,
      providesTags: ["User"],
    }),
    getProducts: build.query({
      query:()=>"products",
      providesTags: ["Products"],
    }),
    getCustomers: build.query({
      query: () => "customers",
      providesTags: ["Customers"],
    }),
    getTransactions: build.query({
      query: ({ page, pageSize, sort, search }) => ({
        url:"transactions",
        method: 'GET',
        params: { page, pageSize, sort, search },
      }),
      providesTags: ["Transactions"],
    }),
    getSales: build.query({
      query: () => "sales",
      providesTags: ["Sales"],
    }),
  }),
})

export const {
  useGetUserQuery, 
  useGetProductsQuery, 
  useGetCustomersQuery, 
  useGetTransactionsQuery,
  useGetSalesQuery,  
} = api;