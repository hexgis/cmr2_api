from django.db.models import (
    Count,
    FloatField,
    F,
    Q,
    Sum,
    functions,
    Value,
    ExpressionWrapper
)


class GroupingClassificationOfStages():
    """Retorn annotate responsible for the:
        Sum of mapped stages according to the grouping performed;
        TI percentage sum of mapped stages according to the grouping performed.
    """
    
    def absolute_number(self,queryset):
        """Add Sum of mapped stages according to the grouping performed to
        queryset
        """
        queryset = queryset.annotate(
            total_nu_area_ha=Sum("nu_area_ha"),
            quantity_polygons=Count(
                "no_estagio", output_field=FloatField()
            ),
            cr_nu_area_ha=functions.Coalesce(Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="CR"),
                output_field=FloatField()), 0.0
            ),
            dg_nu_area_ha=functions.Coalesce(Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="DG"),
                output_field=FloatField()), 0.0
            ),
            dr_nu_area_ha=functions.Coalesce(Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="DR"),
                output_field=FloatField()), 0.0
            ),
            ff_nu_area_ha=functions.Coalesce(Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="FF"),
                output_field=FloatField()), 0.0
            )
        )

        return queryset

    def absolute_number_and_percentage(self, queryset):
        """Add Sum end TI percentage sum of mapped stages according to the
        grouping performed.
        """
        queryset = queryset.annotate(
            total_nu_area_ha=Sum("nu_area_ha"),
            quantity_polygons=Count(
                "no_estagio", output_field=FloatField()
            ),
            cr_nu_area_ha=functions.Coalesce(Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="CR"),
                output_field=FloatField()), 0.0
            ),
            dg_nu_area_ha=functions.Coalesce(Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="DG"),
                output_field=FloatField()), 0.0
            ),
            dr_nu_area_ha=functions.Coalesce(Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="DR"),
                output_field=FloatField()), 0.0
            ),
            ff_nu_area_ha=functions.Coalesce(Sum(
                "nu_area_ha",
                filter=Q(no_estagio__exact="FF"),
                output_field=FloatField()), 0.0
            ),
            cr_nu_area_perc=functions.Coalesce(ExpressionWrapper(
                F('cr_nu_area_ha') / F('ti_nu_area_ha') * Value(100),
                output_field=FloatField()),0.0
            ),
            dg_nu_area_perc=functions.Coalesce(ExpressionWrapper(
                F('dg_nu_area_ha') / F('ti_nu_area_ha') * Value(100),
                output_field=FloatField()),0.0
            ),
            dr_nu_area_perc=functions.Coalesce(ExpressionWrapper(
                F('dr_nu_area_ha') / F('ti_nu_area_ha') * Value(100),
                output_field=FloatField()),0.0
            ),
            ff_nu_area_perc=functions.Coalesce(ExpressionWrapper(
                F('ff_nu_area_ha') / F('ti_nu_area_ha') * Value(100),
                output_field=FloatField()),0.0
            )
        )

        return queryset