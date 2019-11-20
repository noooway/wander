from . import example_data


def init_data_sources(app):
    register_dataframes(app)
    #import_csv(app)
    #import_from_db(app)


def register_dataframes(app):
    app.data_sources = {}
    app.data_sources['revenue'] = example_data.revenue_df
    app.data_sources['regs'] = example_data.regs_df
    app.data_sources['inst_to_regs_conv'] = example_data.inst_to_regs_conv_df
    app.data_sources['first_sales'] = example_data.first_sales_df
    app.data_sources['regs_to_first_sales_conv'] = \
        example_data.regs_to_first_sales_conv_df
    app.data_sources['sales'] = example_data.sales_df
    app.data_sources['first_sales_to_second_sales_conv'] = \
        example_data.first_sales_to_second_sales_conv_df


def import_csv(app):
    pass


def import_from_db(app):
    pass
