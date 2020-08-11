def get_styles():
    #Create all different font styles
    styles = getSampleStyleSheet()
    header_style = styles.add(ParagraphStyle(
        name='header_style',
        fontFamily='Montserrat',
        fontSize=11,
        textColor=colors.HexColor('#FFFFFF')))
    styles['header_style'].alignment = TA_CENTER
    category_style = styles.add(ParagraphStyle(
        name='category_style',
        fontFamily='Fjalla-One',
        fontSize=20,
        leftIndent=13,
        textColor=colors.HexColor('#FFFFFF')))
    styleN = styles.add(ParagraphStyle(
        name='Breadpointlist_style',
        fontFamily='Montserrat',
        fontSize=8,
        leading=12,
        wordWrap='LTR',))
    title_style = styles.add(ParagraphStyle(
        name='title_style',
        fontFamily='Fjalla-One',
        fontSize=30,
        textColor=colors.HexColor("#1ca4bc")))
    subtitle1_style = styles.add(ParagraphStyle(
        name='subtitle1_style',
        fontFamily='Fjalla-One',
        fontSize=12))
    subtitle2_style = styles.add(ParagraphStyle(
        name='subtitle2_style',
        fontFamily='Fjalla-One',
        fontSize=11))
    return styles