import EN from './EN'

type Meta = {
  app?: string | null
  schema?: string | null
  name?: string | null
}

export const Lang = {
  ...EN,
  module(meta: Meta | null, column: string): string {
    try {
      let translate: string | null = null
      if (meta) {
        const { app, schema, name } = meta

        interface MyObject {
          [key: string]: any
        }
        let obj: MyObject | undefined

        if (app && schema && name) {
          if (app == 'crm') obj = this.crm
          if (app == 'finance') obj = this.finance
          if (app == 'identity') obj = this.identity
          if (app == 'hris') obj = this.hris
          if (app == 'project_management') obj = this.project_management
          if (app == 'engineering') obj = this.engineering
          if (app == 'procurement') obj = this.procurement

          if (obj) {
            translate = obj?.[schema]?.[name]?.[column]
          }
        }
      }

      // If translation is not found, replace underscores with spaces
      if (!translate) {
        translate = column.replaceAll(/_/g, ' ')
      }

      return translate
    } catch (error) {
      // In case of any error, fall back to replacing underscores with spaces
      return column.replaceAll(/_/g, ' ')
    }
  }
}
