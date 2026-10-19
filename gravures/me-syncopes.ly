\version "2.24.3"
%% Fichier produit par outils/generer_mesure.py — ne pas modifier à la main.
\paper {
  indent = 0
  paper-width = 152\mm
  line-width = 150\mm
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new Staff { \new Voice {
        \clef treble \autoBeamOff \numericTimeSignature \textLengthOn
        \time 4/4 c''8 d''4^\markup \tiny \italic "syncope" e''8 f''4 g''4~^\markup \tiny \italic "syncope" | g''4 a''2^\markup \tiny \italic "syncope" g''4
        \bar "|."
      } }
  \layout {
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \omit BarNumber }
  }
}
